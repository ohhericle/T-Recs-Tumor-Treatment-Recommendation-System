import math
import boto3
import numpy as np
import pandas as pd


yelp_data = pd.read_csv('s3://trecs-data-s3/data/clean_data/final_yelp_dataset.csv')
oncologist_data = pd.read_csv(
        's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv', 
        encoding='unicode_escape',
        converters={"zip": str}        
)

trecs_data = pd.merge(oncologist_data, yelp_data, on='placekey', how='left')

trecs_data = trecs_data.drop_duplicates(subset=['uuid'])

org_mean_compounds = trecs_data.groupby('org_nm')['compound'].mean().to_dict()

def get_missing_scores(row):
    if np.isnan(row['compound']):
        return org_mean_compounds.get(row['org_nm'], np.NaN)
    return row['compound']

trecs_data['compound'] = trecs_data.apply(get_missing_scores, axis=1)

trecs_data.to_csv('s3://trecs-data-s3/data/final/trecs.csv')
