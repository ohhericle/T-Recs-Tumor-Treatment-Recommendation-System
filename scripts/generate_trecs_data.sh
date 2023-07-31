#!/bin/bash
set -e

echo Preprocessing yelp data...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/preprocess_yelp_data.py
echo Completed preprocessing data. 

echo Running VADER sentiment analysis...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/yelp_sentiment.py
echo Completed sentiment analysis.

echo Combining sentiment datasets...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/yelp_post_sentiment_combiner.py
echo Done combining datasets.

echo Combining sentiment and location datasets...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/yelp_sentiment_location_combiner.py
echo Done combining datasets. 

echo Generating placekeys for yelp dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/generate_yelp_placekeys.py
echo Completed placekey generation for yelp dataset.  

echo Preprocessing provider data...
/home/ec2-user/miniconda3/bin/python python_scripts/providers/preprocess_provider_data.py
echo Completed placekey generation for providers dataset.

echo Generating placekeys for providers dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/providers/generate_provider_placekeys.py
echo Completed placekey generation for providers dataset.

echo Generating T-Recs dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/generate_final_trecs_dataset.py
echo Created final entry point for T-Recs models.

echo Pruning s3 bucket...
aws s3 rm s3://trecs-data-s3/data/business_data --recursive
aws s3 rm s3://trecs-data-s3/data/clean_data --recursive
aws s3 rm s3://trecs-data-s3/data/processed_raw_data --recursive
aws s3 rm s3://trecs-data-s3/data/sentiment_data --recursive
echo Done! Enjoy your data! 
