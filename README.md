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
/data/CellGAT_Input: input directed graphs used in the original manuscript to generate CellGAT results
/data/CellGAT_Output: results from CellGAT inference used in the original publication
/data/models: saved models for each dataset used in the original publication
/data/LR_database: all information used from the Omnipath Database used for CCC predictions
/data/100_times: results from randomization expreiments on each dataset for benchmarking
/data/raw_data: original count matrices from each dataset

    
