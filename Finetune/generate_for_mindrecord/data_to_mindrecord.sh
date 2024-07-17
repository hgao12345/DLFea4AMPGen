##generate mindrecord for finetuning
python generate_seq_for_classification.py 
    --data_dir csv_data
    --vocab_file vocab_v2.txt 
    --output_dir mr_data
    --max_seq_length 1024 
    --do_train True 
    --do_eval True 
    --do_test True


