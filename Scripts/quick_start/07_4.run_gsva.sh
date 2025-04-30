#!/bin/bash

tool_dir=../../SDAS_beta_v2504
binsize=100
h5ad_file=../../output/graphST/sample_graphst.h5ad
output_dir=../../output/gsva
gsva_plan=../../Test_data/single_slice/gsva_plan.csv


# run for all gmt files
${tool_dir}/SDAS geneSetEnrichment gsva -i $h5ad_file -o $output_dir --gsva_plan $gsva_plan --species human
