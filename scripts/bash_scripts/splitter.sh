#!/bin/bash

input_file=/home/ec2-user/capstone/data/raw_data/yelp_contains_doctor.json
lines_per_file=250
output_prefix="output"  # Prefix for the output files

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file not found."
    exit 1
fi

# Create output directory
output_dir="/home/ec2-user/capstone/data/yelp_business_ids_dir/"  # Replace with the desired output directory
mkdir -p "$output_dir"

# Splitting the file
split -l "$lines_per_file" "$input_file" "$output_dir/$output_prefix"

echo "Splitting complete."

