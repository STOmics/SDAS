#!/bin/bash

tool_dir=../../SDAS_beta_v2504
csv_file=../../output/DEG/3.vs.8.wilcoxon.deg_filtered.csv # need to use the differential genes
output_dir=../../output/enrichr


${tool_dir}/SDAS geneSetEnrichment enrichr -i $csv_file -o $output_dir --species human --cut_off 0.05


