#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from warnings import filterwarnings
filterwarnings('ignore')
from matplotlib import pyplot as plt
import numpy as np
import math
#import phenograph
import os, sys, glob, re
import time
import scanpy as sc
import anndata
import scipy
import anndata as ad
from optparse import OptionParser
import time
import math

def create_anndata(geneExpFile, metaFile):
    """
    generate anndata from csv file
    """
    df = pd.read_csv(geneExpFile, sep=",", index_col=0, comment="#") 
    print("read expression file done")
    expMtx = scipy.sparse.csr_matrix(df.T) # cells * genes
    print("generate sparse expression matrix done")
    var = pd.DataFrame(index = df.T.columns) # genes
    obs = pd.read_csv(metaFile, index_col=False, sep=",") 
    print("read meta file done")
    obs = obs.set_index(df.columns) #cells
    adata = anndata.AnnData(X = expMtx, obs = obs, var = var)
    print("create anndata obj done")
    adata.obsm['spatial'] = adata.obs[['x', 'y']].values
    return(adata)

dataDir = './'
geneExpFile = dataDir+'/tmp/counts.csv'
metaFile = dataDir+'/tmp/meta.csv'

adata = create_anndata(geneExpFile, metaFile)

adata.write(dataDir+'/seurat_int_logTotal_10000.h5ad')

adata.var_names

adata.obs

isinstance(adata.X, scipy.sparse.csr_matrix)


# 检查 adata.X 是否是稀疏矩阵
if isinstance(adata.X, scipy.sparse.csr_matrix):
    # 转换为密集矩阵
    dense_matrix = adata.X.toarray()
    print(dense_matrix[:5, :10])  # 查看前 5 行和前 10 列
else:
    print(adata.X[:5, :10])  # 直接查看


if np.isnan(adata.X.toarray()).any():  # 如果是稀疏矩阵，需要先转换为密集矩阵
    print("存在缺失值（NaN）")
else:
    print("没有缺失值")
