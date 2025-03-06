#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
rds_file=$(realpath "../../output/cell2location/sample_standard_anno_cell2location.rds")
output_dir=../../output/cellchat

mkdir -p $output_dir
${tool_dir}/SDAS CCI cellchat -i $rds_file -o $output_dir --bin_size $binsize --label_key anno_cell2location --species human --method truncatedMean --add_spatial
