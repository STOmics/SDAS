#!/bin/bash

tool_dir=../../SDAS_beta
binsize=100
h5ad_file=../../output/graphST/sample_standard_graphst.h5ad
output_dir=../../output/gsea
gsea_plan=../../Test_data/single_slice/gsea_plan.csv


# run for all gmt files
${tool_dir}/SDAS geneSetEnrichment gsea -i $h5ad_file -o $output_dir --gsea_plan $gsea_plan --species human
