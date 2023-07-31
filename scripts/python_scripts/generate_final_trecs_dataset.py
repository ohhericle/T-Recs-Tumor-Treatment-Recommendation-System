import boto3
import pandas as pd


yelp_data = pd.read_csv('s3://trecs-data-s3/data/clean_data/final_yelp_dataset.csv')
oncologist_data = pd.read_csv(
        's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv', 
        encoding='unicode_escape'
)

trecs_data = oncologist_data.merge(yelp_data, on='placekey')

trecs_data.to_csv('s3://trecs-data-s3/data/final/trecs.csv')
