#!/bin/bash


tool_dir=../../SDAS_beta
h5ad_file=../../output/rctd/sample_standard_anno_rctd.h5ad
output_dir=../../output/rctd

mkdir -p $output_dir
${tool_dir}/SDAS dataProcess h5ad2rds -i $h5ad_file -o $output_dir


