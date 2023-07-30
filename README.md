# T-Recs Tumors Treatment Recommendation System

## Prerequisites
In order to run the data pipeline, please set up your environment with the following: 
  1. EC2 instance with RHEL 9 operating system.
  2. Install `jquery` via `sudo yum install jq`.
  3. Install `miniconda3` via the installer.
  4. Install `pandas` and `vaderSentiment` via `pip`.

## Yelp Data Pipeline
To execute the Yelp data pipeline found in the `generate_trecs_data.sh` bash script, run `./generate_trecs_data.sh`. 
This script contains following components:
  1. Preprocess Yelp Dataset
  2. Execute VADER Sentiment Analysis
  3. Collate Yelp Location and Sentiment Data
  4. Integrate Placekeys API 
