[The finetuned model](https://zenodo.org/records/12747957) can be directly used to predict the activity of peptides, including antibacterial activity, anfungal activity, and antioxidant activity. <br><br>

In this step, a total of two columns of data are required in CSV file. The first column is the ID number, with the column name "id"; the second column is the sequence information, with the column name "seq". As shown in the table below：
| id | seq |
| :--:| :--: |
| id1 | seq1 |
| id2 | seq2 |
| id3 | seq3 |


Here, it takes less than 1 minute to predict 100 active peptides. And [the ABP folder](https://github.com/hgao12345/DLFea4AMPGen/tree/main/Prediction/ABP) has been supplemented with example of input data file and model prediction result file. <br><br>
Note: In the prediction results, label "0" represents positive, and label "1" represents negative.
