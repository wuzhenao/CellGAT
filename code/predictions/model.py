import os
import torch
# os.environ['TORCH'] = torch.__version__
# os.system('pip install -q torch-scatter -f https://data.pyg.org/whl/torch-${TORCH}.html')
# os.system('pip install -q torch-sparse -f https://data.pyg.org/whl/torch-${TORCH}.html')
# os.system('pip install -q git+https://github.com/pyg-team/pytorch_geometric.git')


import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from utils import *
import argparse
import os.path as osp
import umap 
import torch
import torch.nn.functional as F
from typing import Optional, Tuple
import scanpy as sc
import torch
from torch import Tensor
from torch.nn import Embedding
from torch.utils.data import DataLoader

from torch_geometric.utils import sort_edge_index
from torch_geometric.utils.num_nodes import maybe_num_nodes
from torch_geometric.utils.sparse import index2ptr

try:
    import torch_cluster  # noqa
    random_walk = torch.ops.torch_cluster.random_walk
except ImportError:
    random_walk = None
from torch_geometric.datasets import Entities
from torch_geometric.nn import FastRGCNConv, RGCNConv, GCNConv, InnerProductDecoder, GAE, VGAE
from torch_geometric.utils import k_hop_subgraph

from torch_geometric.datasets import Planetoid
from torch_geometric.data.data import Data
from torch_geometric.transforms import NormalizeFeatures

# 导入GATv2Conv模型
from torch_geometric.nn import GATConv
from torch_geometric.nn import GATv2Conv

import os.path as osp

import torch
import torch.nn.functional as F
from torch.nn import Parameter
from tqdm import tqdm
from torch_geometric.nn import GAE, RGCNConv

from sklearn.model_selection import train_test_split
from torch_geometric.data import Dataset

from torch_geometric.nn import Node2Vec
import os.path as osp
import torch
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from torch_geometric.datasets import Planetoid
from tqdm.notebook import tqdm

import torch_cluster

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
from torch_geometric.nn import GATConv

from torch_geometric.data import Data 

from scipy.spatial.distance import squareform, pdist
import anndata

class Omnipath_Node2Vec(torch.nn.Module):
    r"""The Node2Vec model from the
    `"node2vec: Scalable Feature Learning for Networks"
    <https://arxiv.org/abs/1607.00653>`_ paper where random walks of
    length :obj:`walk_length` are sampled in a given graph, and node embeddings
    are learned via negative sampling optimization.

    .. note::

        For an example of using Node2Vec, see `examples/node2vec.py
        <https://github.com/pyg-team/pytorch_geometric/blob/master/examples/
        node2vec.py>`_.

    Args:
        edge_index (torch.Tensor): The edge indices.
        embedding_dim (int): The size of each embedding vector.
        walk_length (int): The walk length.
        context_size (int): The actual context size which is considered for
            positive samples. This parameter increases the effective sampling
            rate by reusing samples across different source nodes.
        walks_per_node (int, optional): The number of walks to sample for each
            node. (default: :obj:`1`)
        p (float, optional): Likelihood of immediately revisiting a node in the
            walk. (default: :obj:`1`)
        q (float, optional): Control parameter to interpolate between
            breadth-first strategy and depth-first strategy (default: :obj:`1`)
        num_negative_samples (int, optional): The number of negative samples to
            use for each positive sample. (default: :obj:`1`)
        num_nodes (int, optional): The number of nodes. (default: :obj:`None`)
        sparse (bool, optional): If set to :obj:`True`, gradients w.r.t. to the
            weight matrix will be sparse. (default: :obj:`False`)
    """
    def __init__(
        self,
        edge_index: Tensor,
        embedding_dim: int,
        walk_length: int,
        context_size: int,
        walks_per_node: int = 1,
        p: float = 1.0,
        q: float = 1.0,
        num_negative_samples: int = 1,
        num_nodes: Optional[int] = None,
        sparse: bool = False,
    ):
        super().__init__()

        if random_walk is None:
            raise ImportError('`Node2Vec` requires `torch-cluster`.')

        self.num_nodes = maybe_num_nodes(edge_index, num_nodes)

        row, col = sort_edge_index(edge_index, num_nodes=self.num_nodes).cpu()
        self.rowptr, self.col = index2ptr(row, self.num_nodes), col

        self.EPS = 1e-15
        assert walk_length >= context_size

        self.embedding_dim = embedding_dim
        self.walk_length = walk_length - 1
        self.context_size = context_size
        self.walks_per_node = walks_per_node
        self.p = p
        self.q = q
        self.num_negative_samples = num_negative_samples

        self.embedding = Embedding(self.num_nodes, embedding_dim,
                                   sparse=sparse)

        self.reset_parameters()

    def reset_parameters(self):
        r"""Resets all learnable parameters of the module."""
        self.embedding.reset_parameters()

    def forward(self, batch: Optional[Tensor] = None) -> Tensor:
        """Returns the embeddings for the nodes in :obj:`batch`."""
        emb = self.embedding.weight
        return emb if batch is None else emb.index_select(0, batch)

    def loader(self, **kwargs) -> DataLoader:
        return DataLoader(range(self.num_nodes), collate_fn=self.sample,
                          **kwargs)

    @torch.jit.export
    def pos_sample(self, batch: Tensor) -> Tensor:
        batch = batch.repeat(self.walks_per_node)
        rw = random_walk(self.rowptr, self.col, batch, self.walk_length,
                         self.p, self.q)
        if not isinstance(rw, Tensor):
            rw = rw[0]

        walks = []
        num_walks_per_rw = 1 + self.walk_length + 1 - self.context_size
        for j in range(num_walks_per_rw):
            walks.append(rw[:, j:j + self.context_size])
        return torch.cat(walks, dim=0)

    @torch.jit.export
    def neg_sample(self, batch: Tensor) -> Tensor:
        batch = batch.repeat(self.walks_per_node * self.num_negative_samples)

        rw = torch.randint(self.num_nodes, (batch.size(0), self.walk_length))
        rw = torch.cat([batch.view(-1, 1), rw], dim=-1)

        walks = []
        num_walks_per_rw = 1 + self.walk_length + 1 - self.context_size
        for j in range(num_walks_per_rw):
            walks.append(rw[:, j:j + self.context_size])
        return torch.cat(walks, dim=0)

    @torch.jit.export
    def sample(self, batch: Tensor) -> Tuple[Tensor, Tensor]:
        if not isinstance(batch, Tensor):
            batch = torch.tensor(batch)
        return self.pos_sample(batch), self.neg_sample(batch)

    @torch.jit.export
    def loss(self, pos_rw: Tensor, neg_rw: Tensor) -> Tensor:
        r"""Computes the loss given positive and negative random walks."""

        # Positive loss.
        start, rest = pos_rw[:, 0], pos_rw[:, 1:].contiguous()

        h_start = self.embedding(start).view(pos_rw.size(0), 1,
                                             self.embedding_dim)
        h_rest = self.embedding(rest.view(-1)).view(pos_rw.size(0), -1,
                                                    self.embedding_dim)

        out = (h_start * h_rest).sum(dim=-1).view(-1)
        pos_loss = -torch.log(torch.sigmoid(out) + self.EPS).mean()

        # Negative loss.
        start, rest = neg_rw[:, 0], neg_rw[:, 1:].contiguous()

        h_start = self.embedding(start).view(neg_rw.size(0), 1,
                                             self.embedding_dim)
        h_rest = self.embedding(rest.view(-1)).view(neg_rw.size(0), -1,
                                                    self.embedding_dim)

        out = (h_start * h_rest).sum(dim=-1).view(-1)
        neg_loss = -torch.log(1 - torch.sigmoid(out) + self.EPS).mean()

        return pos_loss + neg_loss

def Omnipath_train(model,loader,optimizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = "cpu"
    model.train()
    total_loss = 0
    for pos_rw, neg_rw in loader:
        optimizer.zero_grad()
        loss = model.loss(pos_rw.to(device), neg_rw.to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

@torch.no_grad()
def Omnipath_test(model,data):
    model.eval()
    z = model()
    acc = model.test(z[data.train_mask], data.y[data.train_mask],
                     z[data.test_mask], data.y[data.test_mask],
                     max_iter=150)
    return acc


class GAT(torch.nn.Module):
    r"""The GATv2 operator from the `"How Attentive are Graph Attention
    Networks?" <https://arxiv.org/abs/2105.14491>`_ paper, which fixes the
    static attention problem of the standard
    :class:`~torch_geometric.conv.GATConv` layer.
    Since the linear layers in the standard GAT are applied right after each
    other, the ranking of attended nodes is unconditioned on the query node.
    In contrast, in :class:`GATv2`, every node can attend to any other node.

    .. math::
        \mathbf{x}^{\prime}_i = \alpha_{i,i}\mathbf{\Theta}_{s}\mathbf{x}_{i} +
        \sum_{j \in \mathcal{N}(i)}
        \alpha_{i,j}\mathbf{\Theta}_{t}\mathbf{x}_{j},

    where the attention coefficients :math:`\alpha_{i,j}` are computed as

    .. math::
        \alpha_{i,j} =
        \frac{
        \exp\left(\mathbf{a}^{\top}\mathrm{LeakyReLU}\left(
        \mathbf{\Theta}_{s} \mathbf{x}_i + \mathbf{\Theta}_{t} \mathbf{x}_j
        \right)\right)}
        {\sum_{k \in \mathcal{N}(i) \cup \{ i \}}
        \exp\left(\mathbf{a}^{\top}\mathrm{LeakyReLU}\left(
        \mathbf{\Theta}_{s} \mathbf{x}_i + \mathbf{\Theta}_{t} \mathbf{x}_k
        \right)\right)}.

    If the graph has multi-dimensional edge features :math:`\mathbf{e}_{i,j}`,
    the attention coefficients :math:`\alpha_{i,j}` are computed as

    .. math::
        \alpha_{i,j} =
        \frac{
        \exp\left(\mathbf{a}^{\top}\mathrm{LeakyReLU}\left(
        \mathbf{\Theta}_{s} \mathbf{x}_i
        + \mathbf{\Theta}_{t} \mathbf{x}_j
        + \mathbf{\Theta}_{e} \mathbf{e}_{i,j}
        \right)\right)}
        {\sum_{k \in \mathcal{N}(i) \cup \{ i \}}
        \exp\left(\mathbf{a}^{\top}\mathrm{LeakyReLU}\left(
        \mathbf{\Theta}_{s} \mathbf{x}_i
        + \mathbf{\Theta}_{t} \mathbf{x}_k
        + \mathbf{\Theta}_{e} \mathbf{e}_{i,k}]
        \right)\right)}.

    Args:
        in_channels (int or tuple): Size of each input sample, or :obj:`-1` to
            derive the size from the first input(s) to the forward method.
            A tuple corresponds to the sizes of source and target
            dimensionalities in case of a bipartite graph.
        out_channels (int): Size of each output sample.
        heads (int, optional): Number of multi-head-attentions.
            (default: :obj:`1`)
        concat (bool, optional): If set to :obj:`False`, the multi-head
            attentions are averaged instead of concatenated.
            (default: :obj:`True`)
        negative_slope (float, optional): LeakyReLU angle of the negative
            slope. (default: :obj:`0.2`)
        dropout (float, optional): Dropout probability of the normalized
            attention coefficients which exposes each node to a stochastically
            sampled neighborhood during training. (default: :obj:`0`)
        add_self_loops (bool, optional): If set to :obj:`False`, will not add
            self-loops to the input graph. (default: :obj:`True`)
        edge_dim (int, optional): Edge feature dimensionality (in case
            there are any). (default: :obj:`None`)
        fill_value (float or torch.Tensor or str, optional): The way to
            generate edge features of self-loops
            (in case :obj:`edge_dim != None`).
            If given as :obj:`float` or :class:`torch.Tensor`, edge features of
            self-loops will be directly given by :obj:`fill_value`.
            If given as :obj:`str`, edge features of self-loops are computed by
            aggregating all features of edges that point to the specific node,
            according to a reduce operation. (:obj:`"add"`, :obj:`"mean"`,
            :obj:`"min"`, :obj:`"max"`, :obj:`"mul"`). (default: :obj:`"mean"`)
        bias (bool, optional): If set to :obj:`False`, the layer will not learn
            an additive bias. (default: :obj:`True`)
        share_weights (bool, optional): If set to :obj:`True`, the same matrix
            will be applied to the source and the target node of every edge,
            *i.e.* :math:`\mathbf{\Theta}_{s} = \mathbf{\Theta}_{t}`.
            (default: :obj:`False`)
        **kwargs (optional): Additional arguments of
            :class:`torch_geometric.nn.conv.MessagePassing`.

    Shapes:
        - **input:**
          node features :math:`(|\mathcal{V}|, F_{in})` or
          :math:`((|\mathcal{V_s}|, F_{s}), (|\mathcal{V_t}|, F_{t}))`
          if bipartite,
          edge indices :math:`(2, |\mathcal{E}|)`,
          edge features :math:`(|\mathcal{E}|, D)` *(optional)*
        - **output:** node features :math:`(|\mathcal{V}|, H * F_{out})` or
          :math:`((|\mathcal{V}_t|, H * F_{out})` if bipartite.
          If :obj:`return_attention_weights=True`, then
          :math:`((|\mathcal{V}|, H * F_{out}),
          ((2, |\mathcal{E}|), (|\mathcal{E}|, H)))`
          or :math:`((|\mathcal{V_t}|, H * F_{out}), ((2, |\mathcal{E}|),
          (|\mathcal{E}|, H)))` if bipartite
    """
    def __init__(self,data,num_classes=3):
        super(GAT, self).__init__()
        self.hid = 5
        self.in_head = 5
        self.out_head = 1
        
        
        self.conv1 = GATv2Conv(data.x.shape[1], self.hid, heads=self.in_head, dropout=0.6)
        self.conv2 = GATv2Conv(self.hid*self.in_head,num_classes, concat=False,
                             heads=self.out_head, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        #x = F.elu(x)
        x = F.sigmoid(x)
        return x