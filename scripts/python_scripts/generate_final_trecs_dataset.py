import boto3
import pandas as pd


yelp_data = pd.read_csv('s3://trecs-data-s3/data/clean_data/final_yelp_dataset.csv')
oncologist_data = pd.read_csv(
#        's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv', 
        'providers/out.csv',
        encoding='unicode_escape',
        converters={"zip": str}        
)

trecs_data = pd.merge(oncologist_data, yelp_data, on='placekey', how='left')

#trecs_data.to_csv('s3://trecs-data-s3/data/final/trecs.csv')
trecs_data.to_csv('trecs.csv')
