# DLFea4AMPGen
By fine-tuning the [pre-trained model MP-BERT](https://github.com/BRITian/MP-BERT), we constructed ABP-MPB model for identifying antibacterial peptides, AFP-MPB model for identifying antifungal peptides, and AOP-MPB model for identifying antioxidant peptides.<br>Based on this, a de novo design strategy for multifunctional antimicrobial peptides was developed.


## Installation
### Huawei Atlas Server (Linux, with Huawei Ascend 910 NPU)
[![](https://img.shields.io/badge/Environment-Docker>=18.03-yellow.svg??style=flat-square)](https://www.docker.com/) <br>
The model construction process uses the MindSpore framework. Installation guide for installing Ascend MindSpore on different hardware platforms can be found at: https://www.mindspore.cn/install/.<br>Here, we recommend to use Docker, an open source application container engine that allows developers to package their applications, as well as dependency packages, into a lightweight, portable container.<br> By using Docker, rapid deployment of MindSpore can be achieved and isolated from the system environment.


## Finetune Task
The overall architecture of the model is shown in the figure below：<br>
![./images/structure.png](https://github.com/hgao12345/DLFea4AMPGen/blob/main/Images/structure.png)

[The pre-trained model](https://zenodo.org/records/12747829) was published in our previous study, and it was trained using publicly available unlabeled pure sequence protein sequences from UniProt. <br>Therefore, the pre-trained model can be directly fine-tuned using the target dataset to construct the desired prediction model.  <br>Here, the fine-tuned framework for classification was used to construct different bioactive models. 
**Fine-tuned models currently available:**
| model	| function |
| :--: 	| :--: |
| [ABP-MPB](https://zenodo.org/records/12747957/files/ABP_Best_Model.ckpt?download=1) | antibacterial activity identification |
| [AFP-MPB](https://zenodo.org/records/12747957/files/AFP_Best_Model.ckpt?download=1) | antifungal activity identification |
| [AOP-MPB](https://zenodo.org/records/12747957/files/AOP_Best_Model.ckpt?download=1) | antioxidant activity identification |

















MP-BERT is trained using publicly available unlabelled pure sequence protein sequences, by self-supervised learning in Figure a.<br>
We train and provide several different pre-trained models with different MP-BERT Hidden Layer sizes, different training data and different data compositions.
A fine-tuned framework for classification, regression and sites prediction is currently available, as shown in Figures b and c.
MP-BERT is based on MindSpore ModelZoo's BERT which has been deeply modified to make it more suitable for protein tasks. Visit the [ModelZoo](https://gitee.com/mindspore/models/tree/master/official/nlp/Bert) page to learn more.

![structure](./images/structure.jpg)

## MP-BERT Pre-training
As MP-BERT needs to be trained on a large dataset, we recommend using a trained pre-trained model or contacting us.<br>
In our study, we used 8 * Ascend 910 32GB computing NPUs, 768GB Memory on a Huawei Atlas 800-9000 training server to complete the training.<br>
The data processing and pre-training code is stored under Pretrain_code and the training data is taken from the UniRef dataset.<br>
Current results for the pre-training task of sequence pairs using Pfamily to establish links between sequences, predicted using the [ProtENN](https://console.cloud.google.com/storage/browser/brain-genomics-public/research/proteins/pfam/random_split) .<br>



**See the Pretrain_code section for more information on the use of pre-training**

## MP-BERT Fine-tuning
Fine tuning can be achieved on one NPU or GPU card
Please load a pre-trained model to achieve fine-tuning according to your needs
**See Finetune_code section for details**

## MP-BERT Fine-tuning downstream tasks
### MPB-PPI
For new information see: [MPB-PPI and MPB-PPISP](https://github.com/BRITian/MPB-PPI-MPB-PPISP) 

### MPB-PPISP
For new information see: [MPB-PPI and MPB-PPISP](https://github.com/BRITian/MPB-PPI-MPB-PPISP) 
