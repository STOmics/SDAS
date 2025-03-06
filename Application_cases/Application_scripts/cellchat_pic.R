library(CellChat)
library(Seurat)
library(patchwork)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

cellchat<-readRDS(args[1])

pdf(args[2])
par(mfrow = c(1,1), xpd=TRUE)
LR.show <-extractEnrichedLR(cellchat, signaling = "PD-L1", geneLR.return = FALSE)
p1<-netVisual_individual(cellchat, signaling = "PD-L1", pairLR.use = LR.show, layout = "chord")
CombinePlots(plots = p1) 
dev.off()
