#!/bin/bash
set -e
clear 

echo Initiating T-Recs Data Pipeline...

echo $'\n________________ Initiating Yelp Data Pipline ________________\n'

echo Preprocessing yelp data...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/preprocess_yelp_data.py
echo $'Completed preprocessing data.\n' 

echo Running VADER sentiment analysis...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/yelp_sentiment.py
echo $'Completed sentiment analysis.\n'

echo Combining sentiment and location datasets...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/yelp_sentiment_location_combiner.py
echo $'Done combining datasets.\n' 

echo Generating placekeys for yelp dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/yelp/generate_yelp_placekeys.py
echo $'Completed placekey generation for yelp dataset.\n'

echo $'\n_________________ Yelp Data Pipline Complete _________________\n'



echo Removing temporary data store...
rm -rf temp_data
echo $'Temporary data store deleted\n'



echo $'\n__________ Initiating Medical Provider Data Pipeline __________\n'

echo Preprocessing provider data...
/home/ec2-user/miniconda3/bin/python python_scripts/providers/preprocess_provider_data.py
echo $'Completed placekey generation for providers dataset.\n'

echo Generating placekeys for providers dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/providers/generate_provider_placekeys.py
echo $'Completed placekey generation for providers dataset.\n'

echo Generating providers dataset...
/home/ec2-user/miniconda3/bin/python python_scripts/providers/generate_final_oncologist_dataset.py
echo $'Completed generation for providers dataset.\n'

echo $'\n___________ Medical Provider Data Pipeline Complete ___________\n'



echo $'\n_____________ Initiating T-Recs Dataset Generation _____________\n'                

/home/ec2-user/miniconda3/bin/python python_scripts/generate_final_trecs_dataset.py
echo $'Created final entry point for T-Recs models.\n'

echo $'\n______________ T-Recs Dataset Generation Complete ______________\n'                



echo Datasets in s3 bucket: 
aws s3 ls s3://trecs-data-s3/data --recursive



echo $'\nPruning s3 bucket...'
aws s3 rm s3://trecs-data-s3/data/business_data --recursive
aws s3 rm s3://trecs-data-s3/data/clean_data --recursive
aws s3 rm s3://trecs-data-s3/data/sentiment_data --recursive
echo Pruning complete.



echo $'\n\nT-Recs Dataset:'
aws s3 ls s3://trecs-data-s3/data/final/ 
echo $'\n\nT-Recs Data Pipeline complete! Enjoy your data!\n\n'
