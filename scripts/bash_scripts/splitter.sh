#!/bin/bash
set -x

input_file=temp_data/processed_raw_data/yelp_contains_doctor.json
lines_per_file=250
output_prefix="output"  # Prefix for the output files

# Create output directory
output_dir="temp_data/processed_raw_data/yelp_business_ids_dir/" 
mkdir -p "$output_dir"

# Splitting the file
split -l "$lines_per_file" "$input_file" "$output_dir/$output_prefix"

echo "Splitting complete."

