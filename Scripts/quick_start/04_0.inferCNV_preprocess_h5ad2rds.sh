#!/bin/bash


tool_dir=../../SDAS_beta_v2504
h5ad_file=../../output/rctd/sample_anno_rctd.h5ad
output_dir=../../output/rctd

${tool_dir}/SDAS dataProcess h5ad2rds -i $h5ad_file -o $output_dir


