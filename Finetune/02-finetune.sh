##finetune_earlystop
python mpbert_classification.py 
--config_path config_1024.yaml 
--do_train True 
--do_eval True 
--description classification 
--num_class 2 
--epoch_num 200 
--early_stopping_rounds 50 
--frozen_bert False 
--device_id id 
--data_url mr_data
--load_checkpoint_url MP-BERT_pretrained_model_1024.ckpt 
--output_url saved_models
--task_name test 
--train_batch_size 32 1> log.log 2> sys.log
