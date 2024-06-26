# CellGAT: A method to predict inter-cell communication in single-cell sequencing data based on graph attention network.

# Install dependent packages
Python packages(pip install -U)                                
    anndata==0.8.0\ liana==0.1.5\ matplotlib==3.6.3\  numpy==1.22.0\ 
    omnipath==1.0.6\  pandas==1.3.5\   rdflib==6.2.0\  scanpy==1.9.1\ 
    scprep==1.2.2\  torch==1.13.1\ leidenalg==0.9.1\  torch-cluster==1.6.1\ 
    torch-scatter -f https://data.pyg.org/whl/torch-1.13.1.html\
    torch-sparse -f https://data.pyg.org/whl/torch-1.13.1.html\
    git+https://github.com/pyg-team/pytorch_geometric.git\

R packages(install.packages("U"))\
    networkD3>=0.4\ dplyr==1.1.4\ htmlwidgets==1.6.4\ webshot==0.5.5\ circlize==0.4.16

# data folder
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c)      /data/CellGAT_Input: input directed graphs used in the original manuscript to generate CellGAT results  
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/50dc8311-09ae-4157-b437-01bac93d2fa8)      /data/CellGAT_Output: results from CellGAT inference used in the original publication    
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/68c9452f-3859-43e3-9300-c00edcae1023)      /data/models: saved models for each dataset used in the original publication   
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/14551e80-5c95-411f-aa9f-164600dfdac6)      /data/LR_database: all information used from the Omnipath Database used for CCC predictions    
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/e7dba5bd-cea9-4599-a8f5-1e7c445e0509)      /data/100_times: results from randomization expreiments on each dataset for benchmarking   
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/5574639c-b4fa-4fe6-92f6-46441d00ca28)      /data/raw_data: original count matrices from each dataset  

# code folder
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/benchmarking:notebooks that will allow you to regenerate figures from the original experiments, benchmarking against other methods and randomization interactions  
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/benchmarking/Drosophila.py:comparison with other methods to identify pathways     
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/preprocessing:notebook that will lead you through how to create the required input for CellGAT inference   
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/100_times:an example script detailing how to run randomization expriments that were conducted for the manuscript   
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/predictions:all utilies and scripts necessary to conduct  CellGAT training and inference  
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/predictions/utils.py: all functions to conduct training processes for  CellGAT (extracting embeddings from the ground truth, computing probabilites using GATv2   
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/predictions/model.py: architecture for both the ground truth Node2Vec and the GATv2  
![image](https://github.com/wuzhenao/CellGAT/assets/114455899/49a2ec9d-8d51-4b1c-afb3-7caacdfa347c) /code/predictions/train.py: script that will, with input created from /code/preprocessing will perform the two step training and inference of CCC by  CellGAT  

Should you have any inquiries or questions, please contact the developer at 2285308398@qq.com




    
