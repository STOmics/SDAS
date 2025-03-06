#!/bin/bash

tool_dir=../../SDAS_beta
h5ad_file=../../Test_data/single_slice/sample.h5ad
output_dir=../../Test_data/single_slice

mkdir -p $output_dir
${tool_dir}/SDAS dataProcess input2h5ad -i $h5ad_file --mode single -o $output_dir
