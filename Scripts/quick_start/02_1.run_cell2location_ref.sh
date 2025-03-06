#!/bin/bash

tool_dir=../../SDAS_beta
ref_file=../../Test_data/single_slice/sample_ref.h5ad
output_dir=../../output/cell2location_ref


#GPU： 
#firstly, use nvidia-smi to check the avalability of gpu, then decide the index of gpu to use
${tool_dir}/SDAS cellAnnotation cell2locationMakeRef --reference $ref_file -o $output_dir --label_key annotation2 --filter_rare_cell 0 --cell_percentage_cutoff2 0.05 --nonz_mean_cutoff 1.45 --gpu_id 0

