#!/bin/bash

tool_dir=../../SDAS_beta
h5ad_file=../../Test_data/single_slice/sample_standard.h5ad
output_dir=../../output/cell2location
ref_csv=../../output/cell2location_ref/sample_ref_inf_aver.csv
binsize=100


#GPU： 
#firstly, use nvidia-smi to check the avalability of gpu, then decide the index of gpu to use
${tool_dir}/SDAS cellAnnotation cell2location -i $h5ad_file -o $output_dir --reference_csv $ref_csv --bin_size $binsize --gpu_id 0
