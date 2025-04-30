#!/bin/bash

tool_dir=../../SDAS_beta_v2504
csv_file=../../output/DEG/3.vs.8.wilcoxon.deg_filtered.csv # need to use all genes
output_dir=../../output/prerank


${tool_dir}/SDAS geneSetEnrichment prerank -i $csv_file --species human -o $output_dir --min_size 3

