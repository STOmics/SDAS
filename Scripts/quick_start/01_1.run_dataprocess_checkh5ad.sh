#!/bin/bash

tool_dir=../../SDAS_beta_v2504
h5ad_file=../../Test_data/single_slice/sample.h5ad
output_dir=../../output/data_process_infor

${tool_dir}/SDAS dataProcess printAdataInfo -i $h5ad_file -o $output_dir
