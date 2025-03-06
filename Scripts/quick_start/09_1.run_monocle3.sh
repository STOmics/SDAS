#!/bin/bash


tool_dir=../../SDAS_beta
binsize=100
rds_file=$(realpath "../../output/rctd/sample_standard_anno_rctd.rds")
output_dir=../../output/monocle3

mkdir -p $output_dir
${tool_dir}/SDAS trajectory monocle3 -i $rds_file -o $output_dir --root_key anno_rctd --root CAF_CXCL14 --gene_color_label pseudotime

