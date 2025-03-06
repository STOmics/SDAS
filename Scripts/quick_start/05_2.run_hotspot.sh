#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../Test_data/single_slice/sample_standard.h5ad
output_dir=../../output/hotspot


${tool_dir}/SDAS coexpress hotspot -i $h5ad_file -o $output_dir --bin_size $binsize --selected_genes top5000 --n_cpus 8
