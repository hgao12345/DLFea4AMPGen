# DLFea4AMPGen
By fine-tuning the [pre-trained model MP-BERT](https://github.com/BRITian/MP-BERT), we constructed ABP-MPB model for identifying antibacterial peptides, AFP-MPB model for identifying antifungal peptides, and AOP-MPB model for identifying antioxidant peptides.<br><br>
Based on this, a de novo design strategy for multifunctional antimicrobial peptides was developed.<br><br>

## Installation
### Huawei Atlas Server (Linux, with Huawei Ascend 910 NPU)
[![](https://img.shields.io/badge/Environment-Docker>=18.03-yellow.svg??style=flat-square)](https://www.docker.com/) <br><br>
The model construction process uses the MindSpore framework. Installation guide for installing Ascend MindSpore on different hardware platforms can be found at: https://www.mindspore.cn/install/.<br><br>
Here, we recommend to use Docker, an open source application container engine that allows developers to package their applications, as well as dependency packages, into a lightweight, portable container.
<br><br> By using Docker, rapid deployment of MindSpore can be achieved and isolated from the system environment.<br><br><br>


## Finetune Task
The overall architecture of the model is shown in the figure below：<br><br>
![./images/structure.png](https://github.com/hgao12345/DLFea4AMPGen/blob/main/Images/structure.png)

[The pre-trained model](https://zenodo.org/records/12747829) was published in our previous study, and it was trained using publicly available unlabeled pure sequence protein sequences from UniProt. <br><br>
Therefore, we can directly fine-tune this pre-trained model to construct the desired prediction model. 
<br><br>Here, the fine-tuned framework for classification was used to construct different bioactive models. <br>
**Fine-tuned models currently available:**
| model	| function |
| :--: 	| :--: |
| [ABP-MPB](https://zenodo.org/records/12747957/files/ABP_Best_Model.ckpt?download=1) | antibacterial activity identification |
| [AFP-MPB](https://zenodo.org/records/12747957/files/AFP_Best_Model.ckpt?download=1) | antifungal activity identification |
| [AOP-MPB](https://zenodo.org/records/12747957/files/AOP_Best_Model.ckpt?download=1) | antioxidant activity identification |

<br><br><br>
## Prediction Task
If you only want to identify AMPs using an existing model rather than constructing a new bioactive peptide prediction model from scratch, you can directly use our model for prediction. <br><br>



