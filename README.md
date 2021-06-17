# User Guide

**Contact:**

dlmu_lab319@163.com

**Citation:** 

Baoshan Ma*, Jianqiao Pan, Xiaoyu Hou, Chongyang Li, Tong Xiong, Yi Gong, Fengju Song*. The Construction of Polygenic Risk Scores for Breast Cancer Based on LightGBM and Multiple Omics Data.(under review)

## 1.Introduction

We provided a python program to generate the PRS of BRCA in your own omics data. The entire process is fully automated without your manual intervention. You only need to enter the type of phenotype and omics data according to the program prompts. For more information about our construction of the PRS model, please refer to “***The Construction of Polygenic Risk Scores for Breast Cancer Basing on LightGBM and Multiple Omics Data***”. If you find the program useful, please cite the above reference.

## 2.Software requirement

The program is built based on python 3.7 version, you can also use a higher version to run this program. We need to use the "os" and "sys" modules to control the interaction between the user and the program, the "joblib" (1.0.1) module to call the trained LightGBM model, and the "numpy" (1.20.1) and "pandas" (1.2.2) modules to calculate the PRS.

## 3.File Directory

The entire folder contains four subfolders and a python program file. The "biological variables" and "saved model" folders contains the csv file of biological variables and the pkl file of trained LightGBM model in four types of omics data for case-control and cancer stage control status. The "input_data" and "output_data" contains omics data provided by the user and PRS of each samples. The "PRS_BRCA.py" is the python program.

## 4.How to use our program

(1) You need to use the `git clone` command to clone the repository to the local, or download it manually.

(2) In the `input_data` folder, you need to upload a csv file of some kind of omics data and name it `data.csv`. In order to speed up the reading of the file, we recommend setting each row as a biological variable and each column as a sample. (If you still use each row as a sample and each column as a biological variable, you need to set paramter `axis` to 1 when calling the `omics_data_load` function.) 

(3) Now, you can run the `PRS_BRCA.py` program. According to the prompt of the console, you need to input the phenotype type and omics data type in turn. The type of phenotype contains `case_control` and `cancer_stage`. The type of omics data contains `methylation`, `miRNA`, `mRNA` and `lncRNA`.

(4) Next, the program will automatically check whether the biological variables match between the input file and the model. If an error prompt is displayed on the console of the program, the user should check the biological variables of the input file according to the prompt.

(5) After the program is executed, you can find the PRS file in the `output_data` folder.

## 5.Example

(1) If we want to obtain the PRS of miRNA data for case-control status, we firstly need to upload a `data.csv` file containing miRNA data (each row is a biological variable and each column is a sample).

(2) Run our "`PRS_BRCA.py`" program. We will see `Please input the status of BRCA:` in the python console, then type `case_control` . Next, We will see `Please input the type of omics data of BRCA:` in the python console, then type `miRNA`. 

(3) After the program is executed, we can find the `TCGA_BRCA_case_control_miRNA_prs.csv` file containing each PRS of sample in the `output_data` folder.
