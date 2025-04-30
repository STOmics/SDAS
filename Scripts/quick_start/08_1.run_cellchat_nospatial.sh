#!/bin/bash

tool_dir=../../SDAS_beta_v2504
binsize=100
rds_file=$(realpath "../../output/cell2location/sample_anno_cell2location.rds")
output_dir=../../output/cellchat_nospatial

${tool_dir}/SDAS CCI cellchat -i $rds_file -o $output_dir --bin_size $binsize --label_key anno_cell2location --gene_symbol_key _index --species human --method truncatedMean
