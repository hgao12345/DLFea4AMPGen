import mindspore as ms
import mindspore.common.dtype as mstype
from src.bert_for_finetune import BertCLS
import numpy as np
from mindspore.train.serialization import load_checkpoint, load_param_into_net
import shap
from transformers import BertTokenizer
import pandas as pd
import argparse
from tqdm import tqdm

from src import tokenization as ms_token
import scipy as sp

class BertConfig:

    def __init__(self,
                 seq_length=1024,
                 vocab_size=25,
                 hidden_size=1024,
                 num_hidden_layers=8,
                 num_attention_heads=16,
                 intermediate_size=3072,
                 hidden_act="gelu",
                 hidden_dropout_prob=0,
                 attention_probs_dropout_prob=0,
                 max_position_embeddings=1024,
                 type_vocab_size=2,
                 initializer_range=0.02,
                 use_relative_positions=False,
                 dtype=mstype.float32,
                 compute_type=mstype.float32):
        self.seq_length = seq_length
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.initializer_range = initializer_range
        self.use_relative_positions = use_relative_positions
        self.dtype = dtype
        self.compute_type = compute_type


def truncate_seq_pair_1x(tokens_a,  max_length):
    total_length = len(tokens_a)
    if total_length <= max_length:
        return tokens_a
    else:
        tokens_a=tokens_a[:max_length]
        return tokens_a

def generate_predict_seq(tokens_a,tokenizer,seq_len):
    tokenizer = ms_token.FullTokenizer(vocab_file="./src/vocab_v2.txt", do_lower_case=False)
    tokens_a = tokenizer.tokenize(tokens_a)
    tokens_a = truncate_seq_pair_1x(tokens_a, seq_len - 3)
    assert len(tokens_a) <= seq_len - 3
    tokens = []
    segment_ids = []
    tokens.append("[CLS]")
    segment_ids.append(0)
    for token in tokens_a:
        tokens.append(token)
        segment_ids.append(0)
    tokens.append("[SEP]")
    segment_ids.append(0)
    assert len(tokens) == len(segment_ids)
    input_ids = ms_token.convert_tokens_to_ids("./src/vocab_v2.txt", tokens)
    input_mask = [1] * len(input_ids)
    while len(input_ids) < seq_len:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)
    assert len(input_ids) == seq_len
    assert len(input_mask) == seq_len
    assert len(segment_ids) == seq_len
    return ms.Tensor([input_ids]),ms.Tensor([input_mask]),ms.Tensor([segment_ids])

def check_output(v,seq):
        tokens=[tokenizer.encode(v, padding='max_length', max_length=1024, truncation=True)]
        input_ids=ms.Tensor(tokens)
        input_mask=(input_ids!=0).astype(mstype.int32)
        segment_ids=ms.Tensor([[0]*1024])
        output_1=model.predict(input_ids, input_mask, segment_ids)[0].asnumpy()
        val_1=sp.special.logit(output_1[1])
        input_ids, input_mask, token_type_id=generate_predict_seq(seq,tokenizer,1024)
        output_2=model.predict(input_ids, input_mask, segment_ids)[0].asnumpy()
        val_2=sp.special.logit(output_2[1])
        print("output_1",output_1)
        print("output_2",output_2)
        print("val_1",val_1)
        print("val_2",val_2)

def f(x):
    vals=[]
    for v in x:
        tokens=[tokenizer.encode(v, padding='max_length', max_length=1024, truncation=True)]
        input_ids=ms.Tensor(tokens)
        input_mask=(input_ids!=0).astype(mstype.int32)
        segment_ids=ms.Tensor([[0]*1024])
        outputs=model.predict(input_ids, input_mask, segment_ids)[0].asnumpy()
        val = sp.special.logit(outputs[1])
        vals.append(val)
    return np.array(vals)


parser = argparse.ArgumentParser()

parser.add_argument('--model', type=str, required=True, help='model from finetune')
parser.add_argument('--input_file', type=str, required=True, help='CSV file containing three columns: id, seq, label')
parser.add_argument('--output_path', type=str, required=True, help='Directory path to save the result file')


args = parser.parse_args()


model=BertCLS(BertConfig(), False, 2)
param_dict = load_checkpoint(args.model)
load_param_into_net(model, param_dict)


tokenizer = BertTokenizer.from_pretrained("./src/vocab_v2.txt", do_lower_case=False)


# Load data
file_data = pd.read_csv("./datasets/data_example.csv")

# Create SHAP Explainer
explainer = shap.Explainer(f, tokenizer)

# Use 'with' to manage file writing and automatically close files
with open(f"{args.output_path}/SHAP_value.txt", "w", encoding="utf-8") as out_value, \
     open(f"{args.output_path}/base_value.txt", "w", encoding="utf-8") as out_base_value, \
     open(f"{args.output_path}/seq.txt", "w", encoding="utf-8") as out_seq:

    # Iterate over each row, use tqdm to show progress bar
    for idx, row in tqdm(file_data.iterrows(), total=len(file_data), desc="Processing sequences"):
        seq_raw = row["seq"]

        # Optional: check model prediction
        check_output(" ".join(list(seq_raw)), seq_raw)

        # Prepare input for SHAP analysis
        seq_formatted = [" ".join(list(seq_raw))]

        # Calculate SHAP values
        shap_values = explainer(seq_formatted, fixed_context=1)

        # Extract values
        val_ = shap_values.values[0]
        base_val_ = shap_values.base_values[0]
        seq_ = shap_values.data[0]

        # Write results
        out_value.write(",".join(map(str, val_)) + "\n")
        out_base_value.write(str(base_val_) + "\n")
        out_seq.write(",".join(seq_) + "\n")

print("All done.")
