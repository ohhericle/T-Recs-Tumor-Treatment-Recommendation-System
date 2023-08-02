import os
import boto3
import subprocess
import pandas as pd
from smart_open import smart_open

def extract_yelp_data():

    '''
    Routine to execute extract_yelp_data.sh, splitter.sh, and runner.sh
    
    inputs:
        None
    
    outputs:
        yelp_bid.csv
        yelp_review_text.txt
        yelp_contains_doctor.json
    '''

    # Extract the yelp data to make yelp_contains_doctor.json and yelp_bid.csv
    subprocess.run(['./bash_scripts/extract_yelp_data.sh'])


def combine_bid_rev(json_path):

    '''
    Combine all the various data joining into one function

    inputs
        yelp_bid.csv (input 1)
        yelp_review_text.txt (input 2)
    '''

    contains_doc = pd.read_json(json_path, lines=True)
    bid_text = contains_doc[['business_id', 'text']]
    bid_text = bid_text.rename(columns={'text': 'review'})

   
    bid_text.to_csv(
        's3://trecs-data-s3/data/clean_data/yelp_bid_reviews.csv', index=False
    )


if __name__ == '__main__':

    contains_doctor_json = 's3://trecs-data-s3/data/raw_data/yelp_contains_doctor.json' 
    extract_yelp_data()
    combine_bid_rev(contains_doctor_json)
