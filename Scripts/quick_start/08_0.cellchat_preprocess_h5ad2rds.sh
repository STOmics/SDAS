#!/bin/bash


tool_dir=../../SDAS_beta
h5ad_file=../../output/cell2location/sample_standard_anno_cell2location.h5ad
output_dir=../../output/cell2location

mkdir -p $output_dir
${tool_dir}/SDAS dataProcess h5ad2rds -i $h5ad_file -o $output_dir


