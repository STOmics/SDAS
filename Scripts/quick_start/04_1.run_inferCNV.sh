#!/bin/bash


tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../output/rctd/sample_standard_anno_rctd.h5ad
rds_file=../../output/rctd/sample_standard_anno_rctd.rds
output_dir=../../output/inferCNV


${tool_dir}/SDAS infercnv -i $rds_file --h5ad $h5ad_file -o $output_dir --bin_size $binsize --label_key anno_rctd --species human --cutoff 0.02 --ref_group_names CAF_CXCL14
# ,CD8_Tem,Endo,Fibro_GPM6B,Fibro_MYH11,Fibro_NOTCH3,Mac_M1,Mac_M2,Mac_SPP1


