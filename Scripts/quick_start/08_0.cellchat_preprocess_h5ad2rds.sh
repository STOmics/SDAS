#!/bin/bash


tool_dir=../../SDAS_beta_v2504
h5ad_file=../../output/cell2location/sample_anno_cell2location.h5ad
output_dir=../../output/cell2location

${tool_dir}/SDAS dataProcess h5ad2rds -i $h5ad_file -o $output_dir


