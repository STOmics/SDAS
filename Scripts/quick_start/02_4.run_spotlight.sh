#!/bin/bash

tool_dir=../../SDAS_beta_v2504
binsize=100
h5ad_file=../../Test_data/single_slice/sample.h5ad
ref_file=../../Test_data/single_slice/sample_ref.h5ad
output_dir=../../output/spotlight


${tool_dir}/SDAS cellAnnotation spotlight -i $h5ad_file -o $output_dir --reference $ref_file --label_key annotation2 --input_gene_symbol_key _index --filter_rare_cell 0 --bin_size $binsize
