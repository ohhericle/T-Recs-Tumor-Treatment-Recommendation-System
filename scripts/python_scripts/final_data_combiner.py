import os
import boto3
import subprocess
import pandas as pd

def combine_bid_loc(bus_contains_doc_path: str):
    
    bus_contains_doc = pd.read_json(bus_contains_doc_path, lines=True)

    bus_contains_doc = bus_contains_doc[bus_contains_doc['is_open'] != 0]
    
    bus_contains_doc = bus_contains_doc.drop(
        columns=['is_open', 'attributes', 'hours', 'review_count', 'stars']
    )
    
    bus_contains_doc.to_csv(
        's3://trecs-data-s3/data/business_data/yelp_bid_loc.csv', index=False
    ) 

def combine_bid_sent_loc(bid_loc_path: str, bid_sent_loc_bname_path: str):
     
    loc_data = pd.read_csv(bid_loc_path)
    sent_data = pd.read_csv(bid_sent_loc_bname_path)
    
    final_yelp_data = sent_data.merge(loc_data, on='business_id')
    final_yelp_data.to_csv('s3://trecs-data-s3/data/final/final_combined_yelp_data.csv', index=False)

if __name__ == '__main__':
    
    subprocess.run(['./bash_scripts/preprocess_location.sh'])    

    bus_contains_doc = 's3://trecs-data-s3/data/business_data/yelp_business_contains_doctor.json'
    bid_loc = 's3://trecs-data-s3/data/business_data/yelp_bid_loc.csv'
    bid_sent_bname = 's3://trecs-data-s3/data/sentiment_data/yelp_bid_sent_name.csv'

    combine_bid_loc(bus_contains_doc)
    combine_bid_sent_loc(bid_loc, bid_sent_bname)
    
    os.system('rm -rf temp_data')    

