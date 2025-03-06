#!/bin/bash

tool_dir=../../SDAS_beta
h5ad_file=../../Test_data/single_slice/sample.h5ad
output_dir=../../output/data_process_infor

mkdir -p $output_dir
${tool_dir}/SDAS dataProcess checkadata -i $h5ad_file -o $output_dir
