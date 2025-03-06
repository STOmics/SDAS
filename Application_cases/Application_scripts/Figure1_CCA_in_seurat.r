library(Seurat)
library(dplyr)
library(ggplot2)
library(HDF5Array)
library(glmGamPoi)
library(zellkonverter)
library(rhdf5)
library(data.table)
library(stringr)
library(repr)

# data dir
input.file <- "../Application_test_data/stereo_bin100_standard.h5ad"
output.dir <- getwd()

# load spatial RNA data from h5ad
sce_RNA <- readH5AD(input.file, use_hdf5 = TRUE, version = '0.9.2', raw = TRUE)
sce_RNA@assays@data$X <- as.matrix(sce_RNA@assays@data$X)
sce_RNA <- as.Seurat(sce_RNA, counts = "X", data = NULL)
sce_RNA = RenameAssays(object = sce_RNA, originalexp = 'RNA')

# spit by sample id
seurat_list <- SplitObject(sce_RNA, split.by = "id")

# normalize and find variable genes for each  sample
seurat_list <- lapply(X = seurat_list, FUN = function(x) {
    x <- NormalizeData(x)
    x <- FindVariableFeatures(x, selection.method = "vst", 
                            nfeatures = 10000) # features可以自行设定
})

# select the features
features <- SelectIntegrationFeatures(object.list = seurat_list, nfeatures = 10000)

print(length(features))

# find the anchors
seurat_anchors <- FindIntegrationAnchors(object.list = seurat_list, 
                                         anchor.features = features, 
                                         dims = 1:30)

print("FindIntegrationAnchors finished")

# integrate the data with anchors
seurat_int <- IntegrateData(anchorset = seurat_anchors, dims = 1:30)

str(seurat_int)

print(seurat_int@assays$integrated@data[1:5,1:5])

print(seurat_int@meta.data[1:5,])

saveRDS(seurat_int,  paste0(output.dir, "/seurat_int_logTotal_10000.rds"))

# Save expression data and obs, which will be loaded in python 
file1 <- paste0(output.dir, '/tmp/counts.csv')
file2 <- paste0(output.dir, '/tmp/meta.csv')
write.csv(seurat_int@assays$integrated@data, file1, row.names=T) 
write.csv(seurat_int@meta.data, file2, row.names=FALSE) ##这里提出来meta.data信息，还有坐标位置的信息

#seurat_int <- readRDS(paste0(output.dir, "/seurat_int_logTotal_10000.rds"))
