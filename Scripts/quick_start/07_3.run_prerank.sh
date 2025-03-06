#!/bin/bash

tool_dir=../../SDAS_beta
csv_file=../../output/DEG/3.vs.8.deg.csv # need to use all genes
output_dir=../../output/prerank


${tool_dir}/SDAS geneSetEnrichment prerank -i $csv_file --species human -o $output_dir

