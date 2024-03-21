# CellGAT: A method to predict inter-cell communication in single-cell sequencing data based on graph attention network.

# Install dependent packages
pip install -U\
    anndata==0.8.0 
    liana==0.1.5 
    matplotlib==3.6.3 
    numpy==1.22.0 
    omnipath==1.0.6 
    pandas==1.3.5 
    rdflib==6.2.0 
    scanpy==1.9.1 
    scprep==1.2.2 
    torch==1.13.1
    leidenalg==0.9.1 
    torch-cluster==1.6.1
    
pip install torch-scatter -f https://data.pyg.org/whl/torch-1.13.1.html
pip install torch-sparse -f https://data.pyg.org/whl/torch-1.13.1.html
pip install git+https://github.com/pyg-team/pytorch_geometric.git
    
