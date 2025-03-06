#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../Test_data/single_slice/sample_standard.h5ad
output_dir=../../output/graphST

mkdir -p $output_dir
#GPU： 
#firstly, use nvidia-smi to check the avalability of gpu, then decide the index of gpu to use
${tool_dir}/SDAS spatialDomain graphst -i $h5ad_file -o $output_dir --gpu_id 0 --tool mclust --n_clusters 10 --n_hvg 3000 --bin_size $binsize
