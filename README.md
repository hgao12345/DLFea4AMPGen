# DLFea4AMPGen
By fine-tuning the [pre-trained model MP-BERT](https://github.com/BRITian/MP-BERT), we constructed ABP-MPB model for identifying antibacterial peptides, AFP-MPB model for identifying antifungal peptides, and AOP-MPB model for identifying antioxidant peptides.<br><br>
Based on this, a de novo design strategy for multifunctional antimicrobial peptides was developed.<br><br>

## Installation
### Huawei Atlas Server (Linux, with Huawei Ascend 910 NPU)
[![](https://img.shields.io/badge/Environment-Docker>=18.03-yellow.svg??style=flat-square)](https://www.docker.com/) <br><br>
The model construction process uses the MindSpore framework. Installation guide for installing Ascend MindSpore on different hardware platforms can be found at: https://www.mindspore.cn/install/.<br><br>
Here, we recommend to use Docker, an open source application container engine that allows developers to package their applications, as well as dependency packages, into a lightweight, portable container.
<br><br> By using Docker, rapid deployment of MindSpore can be achieved and isolated from the system environment.<br><br>


## Finetune Task
The overall architecture of the model is shown in the figure below：<br><br>
<img src="https://github.com/hgao12345/DLFea4AMPGen/blob/main/Images/structure.png" alt="Model Structure" width="500">


[The pre-trained model](https://zenodo.org/records/12747829) was published in our previous study, and it was trained using publicly available unlabeled pure sequence protein sequences from UniProt. <br><br>
Therefore, we can directly fine-tune this pre-trained model to construct the desired prediction model. 
<br><br>
We have fine-tuned the framework for classification to create three bioactive models: ABP-MPB, AFP-MPB, and AOP-MPB. The details are as follows:
| model	| function |
| :--: 	| :--: |
| [ABP-MPB](https://zenodo.org/records/12747957/files/ABP_Best_Model.ckpt?download=1) | Antibacterial activity identification |
| [AFP-MPB](https://zenodo.org/records/12747957/files/AFP_Best_Model.ckpt?download=1) | Antifungal activity identification |
| [AOP-MPB](https://zenodo.org/records/12747957/files/AOP_Best_Model.ckpt?download=1) | Antioxidant activity identification |


## Prediction Task
If you want to identify bioactive peptides using an existing model, you can directly use one of our fine-tuned models without the need to construct a new prediction model from scratch. <br>
### Data Preparation
A total of two columns of data are required in CSV file. The first column is the ID number, with the column name "id"; the second column is the sequence information, with the column name "seq". As shown in the table below：
| id | seq |
| :--:| :--: |
| id1 | seq1 |
| id2 | seq2 |
| id3 | seq3 |

Note: In the prediction results, label "0" represents positive, and label "1" represents negative.

## Sequence Generation
Once the pre-built model is ready and the environment is properly configured, follow these steps sequentially to generate the sequences from scratch.
### SHAP value extraction
Run the following command to extract SHAP values:
```
python SHAP_value.py
```
### Sliding window
Normalize the SHAP value extraction results for each model to compute relative values. This step helps mitigate potential biases caused by large differences in the magnitude of results across different models:
```
python shap_value_normalization.py
```
Set a sliding window of 13 amino acids and retain the window with the highest average SHAP value, provided that it is greater than 0, for each sequence：
```
python sliding_windows_13AA.py
```
