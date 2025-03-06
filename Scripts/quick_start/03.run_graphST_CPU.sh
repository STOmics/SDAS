#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../Test_data/single_slice/sample_standard.h5ad
output_dir=../../output/graphST

mkdir -p $output_dir

${tool_dir}/SDAS spatialDomain graphst -i $h5ad_file -o $output_dir --tool mclust --n_clusters 10 --n_hvg 3000 --bin_size $binsize
