# Classification

First, you need to organize the training data into the following format:

> root_data_path <br>
&emsp;&emsp;|---train.csv <br>
&emsp;&emsp;|---val.csv (Optional) <br>
&emsp;&emsp;|---test.csv (Optional) <br>

Each csv file needs to contain the following columns：

| id | seq | label |
| :--: 	| :--: | :--:	 |
| protein id | protein sequence | int label |


After that, you need to organize the data into Record format：
```
python generate_seq_for_classification.py --data_dir <csv_data> --vocab_file vocab_v2.txt --output_dir <mr_data> --max_seq_length 1024 --do_train True --do_eval True --do_test True
```

Then, use the following scirpt to train and evaluate model:
```
python mpbert_classification.py --config_path config_1024.yaml --do_train True --do_eval True --description classification --num_class 2 --epoch_num 200 --early_stopping_rounds 50 --frozen_bert False --device_id id --data_url <mr_data> --load_checkpoint_url MP-BERT_pretrained_model_1024.ckpt --output_url <saved_models> --task_name test --train_batch_size 32 1> log.log 2> sys.log
```


