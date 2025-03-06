#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../output/graphST/sample_standard_graphst.h5ad
output_dir=../../output/DEG
deg_plan=../../Test_data/single_slice/deg_plan.csv


${tool_dir}/SDAS DEG -i $h5ad_file -o $output_dir --diff_plan $deg_plan
