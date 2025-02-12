import mindspore.nn as nn
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.ops import composite as C
from mindspore.common.tensor import Tensor
from mindspore.common import dtype as mstype
from .bert_for_training import clip_grad
from .finetune_eval_model import BertCLSModel, BertSEQModel, BertSEQModelEval,BertCLSModelEval,BertRegModel
from .utils import CrossEntropyCalculation,FocalLossCalculation,CrossEntropyCalculationV2
import os

GRADIENT_CLIP_TYPE = 1
GRADIENT_CLIP_VALUE = 1.0
grad_scale = C.MultitypeFuncGraph("grad_scale")
reciprocal = P.Reciprocal()


@grad_scale.register("Tensor", "Tensor")
def tensor_grad_scale(scale, grad):
    return grad * reciprocal(scale)


_grad_overflow = C.MultitypeFuncGraph("_grad_overflow")
grad_overflow = P.FloatStatus()


@_grad_overflow.register("Tensor")
def _tensor_grad_overflow(grad):
    return grad_overflow(grad)


class BertFinetuneCell(nn.TrainOneStepWithLossScaleCell):
    def __init__(self, network, optimizer, scale_update_cell=None):
        super(BertFinetuneCell, self).__init__(network, optimizer, scale_update_cell)
        self.cast = P.Cast()

    def construct(self,
                  input_ids,
                  input_mask,
                  token_type_id,
                  label_ids,
                  sens=None):
        """Bert Finetune"""

        weights = self.weights
        loss = self.network(input_ids,
                            input_mask,
                            token_type_id,
                            label_ids)
        if sens is None:
            scaling_sens = self.scale_sense
        else:
            scaling_sens = sens

        status, scaling_sens = self.start_overflow_check(loss, scaling_sens)
        grads = self.grad(self.network, weights)(input_ids,
                                                 input_mask,
                                                 token_type_id,
                                                 label_ids,
                                                 self.cast(scaling_sens,
                                                           mstype.float32))
        grads = self.hyper_map(F.partial(grad_scale, scaling_sens), grads)
        grads = self.hyper_map(F.partial(clip_grad, GRADIENT_CLIP_TYPE, GRADIENT_CLIP_VALUE), grads)
        if self.reducer_flag:
            grads = self.grad_reducer(grads)
        cond = self.get_overflow_status(status, grads)
        overflow = self.process_loss_scale(cond)
        if not overflow:
            self.optimizer(grads)
        return (loss, cond)

class BertCLS(nn.Cell):
    """
    Train interface for classification finetuning task.
    """

    def __init__(self, config, is_training, num_labels=2, dropout_prob=0.0, use_one_hot_embeddings=False,
                 assessment_method=""):
        super(BertCLS, self).__init__()
        self.bert = BertCLSModel(config, is_training, num_labels, dropout_prob, use_one_hot_embeddings,
                                 assessment_method)
        self.loss = CrossEntropyCalculation(is_training)
        self.num_labels = num_labels
        self.assessment_method = assessment_method
        self.is_training = is_training

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits = self.bert(input_ids, input_mask, token_type_id)
        if self.is_training:
            loss = self.loss(logits, label_ids, self.num_labels)
            return loss
        else:
            return logits

    def predict(self, input_ids, input_mask, token_type_id):
        logits = self.bert(input_ids, input_mask, token_type_id)
        return logits



class BertOptimisation(nn.Cell):
    """
    Train interface for classification finetuning task.
    """

    def __init__(self, config, is_training, num_labels=2, dropout_prob=0.0, use_one_hot_embeddings=False,
                 assessment_method=""):
        super(BertOptimisation, self).__init__()
        self.bert = BertSEQModel(config, is_training, num_labels, dropout_prob, use_one_hot_embeddings,
                                 assessment_method)
        self.loss = CrossEntropyCalculationV2(is_training)
        self.num_labels = num_labels
        self.assessment_method = assessment_method
        self.is_training = is_training

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits = self.bert(input_ids, input_mask, token_type_id)
        if self.is_training:
            loss = self.loss(logits, label_ids,input_mask, self.num_labels)
            return loss
        else:
            return logits




class BertReg(nn.Cell):
    """
    Train interface for classification finetuning task.
    """

    def __init__(self, config, is_training, num_labels=1, dropout_prob=0.0, use_one_hot_embeddings=False,
                 assessment_method=""):
        super(BertReg, self).__init__()
        self.bert = BertRegModel(config, is_training, num_labels, dropout_prob, use_one_hot_embeddings,
                                 assessment_method)
        self.loss = CrossEntropyCalculation(is_training)
        self.num_labels = num_labels
        self.assessment_method = assessment_method
        self.is_training = is_training
        self.mse=nn.MSELoss()

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits = self.bert(input_ids, input_mask, token_type_id)
        if self.is_training:
            loss = self.mse(logits, label_ids)
        else:
            loss = logits * 1.0
        return loss


class BertCLSEval(nn.Cell):
    """
    Train interface for classification finetuning task.
    """

    def __init__(self, config, is_training, num_labels=2, dropout_prob=0.0, use_one_hot_embeddings=False,
                 assessment_method=""):
        super(BertCLSEval, self).__init__()
        self.bert = BertCLSModelEval(config, is_training, num_labels, dropout_prob, use_one_hot_embeddings,
                                 assessment_method)
        self.loss = CrossEntropyCalculation(is_training)
        self.num_labels = num_labels
        self.assessment_method = assessment_method
        self.is_training = is_training

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits,pooled_output,sequence_output,all_polled_output,all_sequence_output = self.bert(input_ids, input_mask, token_type_id)
        if self.assessment_method == "spearman_correlation":
            if self.is_training:
                loss = self.loss(logits, label_ids)
            else:
                loss = logits
        else:
            loss = self.loss(logits, label_ids, self.num_labels)
        return loss,pooled_output,sequence_output,all_polled_output,all_sequence_output

class BertSeq(nn.Cell):
    """
    Train interface for sequence labeling finetuning task.
    """

    def __init__(self, config,  is_training, num_labels=11, with_lstm=False,
                 dropout_prob=0.0, use_one_hot_embeddings=False,loss_func="CrossEntropy",label_percent=None,loss_gama=2.0):
        super(BertSeq, self).__init__()
        self.bert = BertSEQModel(config, is_training, num_labels,  with_lstm, dropout_prob,
                                 use_one_hot_embeddings)
        if loss_func=="CrossEntropy":
            self.loss = CrossEntropyCalculation(is_training)
        elif loss_func=="Focal":
            self.loss = FocalLossCalculation(weight=Tensor(label_percent), gamma=loss_gama, reduction='mean',is_training=is_training)
        else:
            raise "Error Loss Name"
        self.loss_name=loss_func
        self.num_labels = num_labels

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits = self.bert(input_ids, input_mask, token_type_id)
        loss = self.loss(logits, label_ids, self.num_labels)

        return loss



class BertSeqEval(nn.Cell):
    """
    Train interface for sequence labeling finetuning task.
    """

    def __init__(self, config,  is_training, num_labels=11, with_lstm=False,
                 dropout_prob=0.0, use_one_hot_embeddings=False,loss_func="CrossEntropy",label_percent=None,loss_gama=2.0):
        super(BertSeqEval, self).__init__()
        self.bert = BertSEQModelEval(config, is_training, num_labels,  with_lstm, dropout_prob,
                                 use_one_hot_embeddings)
        if loss_func=="CrossEntropy":
            self.loss = CrossEntropyCalculation(is_training)
        elif loss_func=="Focal":
            self.loss = FocalLossCalculation(weight=Tensor(label_percent), gamma=loss_gama, reduction='mean',is_training=is_training)
        else:
            raise "Error Loss Name"
        self.loss_name=loss_func
        self.num_labels = num_labels

    def construct(self, input_ids, input_mask, token_type_id, label_ids):
        logits,sequence_output = self.bert(input_ids, input_mask, token_type_id)
        loss = self.loss(logits, label_ids, self.num_labels)

        return loss,sequence_output


from mindspore.train.callback import Callback

class EarlyStoppingSaveBest(Callback):
    def __init__(self, model, ds_val, early_stopping_rounds, save_checkpoint_path):
        super(EarlyStoppingSaveBest, self).__init__()
        self.model = model
        self.ds_val = ds_val
        self.best_acc = 0.0
        self.best_epoch = 0
        self.early_stopping_rounds = early_stopping_rounds
        self.rounds_no_improve = 0
        self.save_checkpoint_path = save_checkpoint_path

    def epoch_end(self, run_context):
        acc = self.model.eval(self.ds_val, ["Accuracy"])
        if acc > self.best_acc:
            self.best_acc = acc
            self.best_epoch = self.cur_epoch_num
            self.rounds_no_improve = 0
            self.model.save_checkpoint(os.path.join(self.save_checkpoint_path, f"best.ckpt"))
            print(f"New best accuracy: {self.best_acc}, saved best model.")
        else:
            self.rounds_no_improve += 1
            print(f"No improvement in accuracy for {self.rounds_no_improve} epochs.")
        if self.rounds_no_improve >= self.early_stopping_rounds:
            print("Early stopping due to no improvement.")
            run_context.request_stop()



