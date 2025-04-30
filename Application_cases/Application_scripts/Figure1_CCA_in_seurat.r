library(Seurat)
library(dplyr)
library(ggplot2)
library(data.table)
library(stringr)
library(repr)

# data dir
#input.file <- "/storeData/USER/data/02.Bioinformatics_for_STOmics/01.user/qiuying/05.SDAS/00.data/01.paper_data/CRC_NC/sdas_rerun_beta2_20250421/rawdata/stereo_bin100.rds"
input.file <- "../Application_test_data/stereo_bin100.rds"
output.dir <- getwd()

# load spatial RNA data from rds
sce_RNA <- readRDS(input.file)

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

# create a temporary folder
tmp_folder <- paste0(output.dir, "/tmp")
if (!dir.exists(tmp_folder)) {
  dir.create(tmp_folder)
  cat("Folder", tmp_folder, "has been created successfully.\n")
} else {
  cat("Folder", tmp_folder, "already exists.\n")
}

# Save expression data and obs, which will be loaded in python 
file1 <- paste0(output.dir, '/tmp/counts.csv')
file2 <- paste0(output.dir, '/tmp/meta.csv')
write.csv(seurat_int@assays$integrated@data, file1, row.names=T) 
write.csv(seurat_int@meta.data, file2, row.names=FALSE) ##这里提出来meta.data信息，还有坐标位置的信息

#seurat_int <- readRDS(paste0(output.dir, "/seurat_int_logTotal_10000.rds"))
