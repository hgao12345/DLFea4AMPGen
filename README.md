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
Once the pre-built model is ready and the environment is properly configured, [follow these steps sequentially to generate the sequences from scratch](https://github.com/hgao12345/DLFea4AMPGen/tree/main/Sequence_Generation).
### Important Environment Recommendation

To **maximize performance for both model training and SHAP value extraction**, we recommend a two-environment setup:

1. **Train and fine-tune your model** inside a Docker environment with Ascend NPU support — ideal for efficient model training.
2. **Sequence Generation** outside the Docker container in a separate environment - starting from [SHAP value Extracting](https://github.com/shap/shap.git).

### SHAP value extraction
Run the following command to extract SHAP values. A total of three files are generated: [seq.txt](https://github.com/hgao12345/DLFea4AMPGen/blob/main/Sequence_Generation/00-SHAP/output/seq.txt), [base_value.txt](https://github.com/hgao12345/DLFea4AMPGen/blob/main/Sequence_Generation/00-SHAP/output/base_value.txt), and [SHAP_value.txt](https://github.com/hgao12345/DLFea4AMPGen/blob/main/Sequence_Generation/00-SHAP/output/SHAP_value.txt). The SHAP_value.txt file contains the SHAP values extracted by the model for each amino acid, with each amino acid assigned a corresponding SHAP value. This file is the primary focus of our analysis.
```
python SHAP_value.py --model <Finetuned model> --input_file <sequence.csv> --output_path <output_path>
```
**Parameters:**

- `--model`: Path to the fine-tuned BERT model checkpoint (e.g., `.ckpt` file).
- `--input_file`: A CSV file with a column named `seq`, where each row is an amino acid sequence.
- `--output_path`: Directory where output files (`SHAP_value.txt`, `base_value.txt`, `seq.txt`) will be saved.
---
### Sliding window
The sliding window process is illustrated in the figure below：<br><br>
<img src="https://github.com/hgao12345/DLFea4AMPGen/blob/main/Images/sliding_windows_Diagram.png" alt="Model Structure" width="500">

**If you are generating single-activity peptides, you can skip this normalization step**. Normalize SHAP values across multiple models to mitigate differences in magnitude, enabling fair comparison or integration. This is particularly useful for multi-model ensemble workflows:
```
python shap_value_normalization.py --input_files <file1.txt> <file2.txt> <file3.txt> --output_path <output_path>
```
**Parameters:**

- `--input_files`: A list of one or more text files containing SHAP values. Each line in a file should represent the SHAP values for a single sequence, with one SHAP value per amino acid.
- `--output_path`: Directory where the results will be saved.
<br><br>

Set a sliding window of 13 amino acids and retain the window with the highest average SHAP value, provided that it is greater than 0, for each sequence：
```
python sliding_windows.py --SHAP_file <SHAP_value.txt> --seq_file <sequence.csv> --length <length> --output_path <output_path>
```
**Parameters:**

- `--SHAP_file`: Path to the file containing SHAP values (e.g., `SHAP_value.txt`) where each row corresponds to one sequence, and each value corresponds to one amino acid.
- `--seq_file`: The CSV file containing the original sequences (`seq` column required), which should match the SHAP values by order.
- `--length`: Length of the sliding window to apply (default is 13 amino acids).
- `--output_path`: Directory where the extracted motifs or windowed sequences will be saved.
---
### Phylogenetic tree
Build the phylogenetic tree with the following command:
```
bash tree.sh <motif.fasta> <tree.newick>
```
**Parameters:**

- `<motif.fasta>`: Input FASTA file containing sequences to be used for tree construction.
- `<tree.newick>`: Output file name for the generated phylogenetic tree in Newick format.

---
### Systematic shuffle
Systematically generate all possible combinations of key high-frequency amino acids for each group to obtain a set of candidate sequences:
```
python systematic_shuffle.py --input_file <amino_acids.csv> --length <motif_length> --output_path <output_path>
```
**Parameters:**

- `--input_file <amino_acids.csv>`: CSV file listing key amino acids for each position to be shuffled and combined.
- `--length <motif_length>`: The length of the motif or peptide to be generated.
- `--output_path <output_path>`: Directory where the generated candidate sequences in FASTA format will be saved.
---
### Representative sequence
Use the [iFeature software](https://github.com/Superzchen/iFeature/) to cluster all sequences from each group. After configuring the environment, execute the following code to complete this process:
```
python iFeature.py <shuffle.fasta>
```
Systematically generate all possible combinations of key high-frequency amino acids for each group to obtain a set of candidate sequences:
```
python centroid.py --input_file <example_data.csv> --output_path <output_path> --random_seed 1 --n_clusters <n_clusters>
```
**Parameters:**

- `--input_file <example_data.csv>`: CSV file containing features or sequences to be clustered.
- `--output_path <output_path>`: Directory to save clustering results.
- `--random_seed 1`: (Optional) Random seed for reproducibility.
- `--n_clusters <n_clusters>`: Number of clusters to generate based on the features extracted by `iFeature.py`.
---
