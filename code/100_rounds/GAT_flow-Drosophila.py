#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import liana as li
import anndata
import scanpy as sc
#from openproblems import tasks
import os 


# In[2]:


# Install required packages.
import os
import torch
os.environ['TORCH'] = torch.__version__
print(torch.__version__)

# !pip install -q torch-scatter -f https://data.pyg.org/whl/torch-${TORCH}.html
# !pip install -q torch-sparse -f https://data.pyg.org/whl/torch-${TORCH}.html
# !pip install -q git+https://github.com/pyg-team/pytorch_geometric.git

# Helper function for visualization.
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from utils import *


# In[3]:


import argparse
import os.path as osp

import torch
import torch.nn.functional as F

from torch_geometric.datasets import Entities
from torch_geometric.nn import FastRGCNConv, RGCNConv, GCNConv, InnerProductDecoder, GAE, VGAE
from torch_geometric.utils import k_hop_subgraph

from torch_geometric.datasets import Planetoid
from torch_geometric.data.data import Data
from torch_geometric.transforms import NormalizeFeatures


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
import random
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

from scipy.io import mmread


# # Pre-processing from original matrix
# 

# In[4]:


#matrix = pd.read_csv("../data/GSE95025/GSM2494785_dge_mel_rep3.txt",sep="\t")
matrix_list = []
common_genes = []
for i,j in zip(range(3,8),range(5,10)):
    matrix_list.append(pd.read_csv(f"/home/tjzhang01/wuzhenao/CellGATv2/data/raw_data/Drosophila/GSM249478{j}_dge_mel_rep{i}.txt",sep="\t",index_col=0))
    if not common_genes:
        common_genes = pd.read_csv(f"/home/tjzhang01/wuzhenao/CellGATv2/data/raw_data/Drosophila/GSM249478{j}_dge_mel_rep{i}.txt",sep="\t",index_col=0).index.tolist()
    else:
        common_genes = list(set(common_genes) & set(pd.read_csv(f"/home/tjzhang01/wuzhenao/CellGATv2/data/raw_data/Drosophila/GSM249478{j}_dge_mel_rep{i}.txt",sep="\t",index_col=0).index.tolist()))
        #matrix_list = [i.loc[common_genes] for i in matrix_list]
matrix = pd.concat(matrix_list)


# In[ ]:


matrix = matrix.loc[common_genes]
matrix = matrix[~matrix.index.duplicated(keep='first')]


# In[ ]:


matrix.index = [str(i).upper() for i in matrix.index.tolist()]


# In[ ]:


from scipy.stats import wilcoxon
import anndata
import scanpy as sc


# In[ ]:


index = matrix.index.tolist()


# In[ ]:


matrix = matrix.fillna(0)


matrix,meta,nodes,interactions,LR_nodes,Omnipath_network = make_nodes_interactions(matrix)

if (Omnipath_network["Src"].dtype != 'float64') and (Omnipath_network["Src"].dtype != 'int64'):
    LR_nodes.index = LR_nodes["identifier"].tolist()
    LR_nodes["Id"] = range(0,LR_nodes.shape[0])
    Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["Id"].tolist()
    Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["Id"].tolist()
Omnipath_data,Omnipath_nodes,Omnipath_interactions = make_dataset(LR_nodes,Omnipath_network,first=False,pathway_encode=False)
Omnipath_nodes.index = Omnipath_nodes["Id"].tolist()

    
    
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = "cpu"
LR_nodes = pd.read_csv("/home/tjzhang01/wuzhenao/CellGATv2/data/LR_database/intercell_nodes_updated.csv",index_col=0)
Omnipath_network = pd.read_csv("/home/tjzhang01/wuzhenao/CellGATv2/data/LR_database/intercell_interactions.csv",index_col=0)
LR_nodes.index = LR_nodes["Id"].tolist()

new_identifier = [row["identifier"] + "_" + row["category"] for index,row in LR_nodes.iterrows()]

LR_nodes["identifier"] = new_identifier

Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["identifier"].tolist()
Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["identifier"].tolist()

ligand_list = Omnipath_network["Src"].tolist()
receptor_list = Omnipath_network["Dst"].tolist()


LR_nodes = LR_nodes[(LR_nodes["identifier"].isin(ligand_list)) | (LR_nodes["identifier"].isin(receptor_list))]

Omnipath_network = Omnipath_network[(Omnipath_network["Src"].isin(LR_nodes["identifier"].tolist())) & (Omnipath_network["Dst"].isin(LR_nodes["identifier"].tolist()))]

LR_nodes["Id"] = range(0,LR_nodes.shape[0])

LR_nodes.index = LR_nodes["identifier"].tolist()
Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["Id"].tolist()
Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["Id"].tolist()

LR_nodes = LR_nodes[(LR_nodes["Id"].isin(Omnipath_network["Src"].tolist())) | (LR_nodes["Id"].isin(Omnipath_network["Dst"].tolist()))]

LR_nodes.index = LR_nodes["Id"].tolist()
Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["identifier"].tolist()
Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["identifier"].tolist()

LR_nodes.index = LR_nodes["identifier"].tolist()
LR_nodes["Id"] = range(0,LR_nodes.shape[0])
Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["Id"].tolist()
Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["Id"].tolist()


df_list = []
Omnipath_network["Src"] = Omnipath_network["Src"].sample(frac=1).tolist()
Omnipath_network["Dst"] = Omnipath_network["Dst"].sample(frac=1).tolist()
for i in range(100):
    print(i)
    if (Omnipath_network["Src"].dtype != 'float64') and (Omnipath_network["Src"].dtype != 'int64'):
        LR_nodes.index = LR_nodes["identifier"].tolist()
        LR_nodes["Id"] = range(0,LR_nodes.shape[0])
        Omnipath_network["Src"] = LR_nodes.loc[Omnipath_network["Src"].tolist()]["Id"].tolist()
        Omnipath_network["Dst"] = LR_nodes.loc[Omnipath_network["Dst"].tolist()]["Id"].tolist()
    df = get_Omnipath_embeddings(LR_nodes,Omnipath_network)
    interactions["Src"] = interactions["Src"].sample(frac=1).tolist()
    interactions["Dst"] = interactions["Dst"].sample(frac=1).tolist()  
    Omnipath_nodes.index = Omnipath_nodes["identifier"].tolist()
    df_list.append(get_cell_LR_embeddings(matrix,meta,nodes,interactions,df,Omnipath_nodes,Omnipath_interactions))

for i in range(len(df_list)):
    temp = df_list[i]
    temp = temp.head(1000)
    temp.to_csv(f"/home/tjzhang01/wuzhenao/CellGATv2/data/CellGATv2_random_data/Drosophila/Drosophila_{i+1}_random.csv")

