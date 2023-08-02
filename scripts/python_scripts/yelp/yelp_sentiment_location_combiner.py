import os
import boto3
import subprocess
import pandas as pd

def get_bid_contains_doc_csv(json_path: str, csv_path: str):
    
    contains_doc = pd.read_json(json_path, lines=True)
    contains_doc = contains_doc[contains_doc['is_open'] != 0]
    
    contains_doc = contains_doc.drop(
        columns=['is_open', 'attributes', 'hours', 'review_count', 'stars']
    )
    contains_doc = contains_doc.drop_duplicates(subset='business_id')    
    
    contains_doc.to_csv(csv_path, index=False) 


def combine_yelp_sent_loc_data(bid_loc: str, bid_sent: str, final_data: str):
     
    loc_data = pd.read_csv(bid_loc)
    sent_data = pd.read_csv(bid_sent)
     
    final_yelp_data = loc_data.merge(sent_data, on='business_id', how='left')
    final_yelp_data = clean_categories(final_yelp_data)

    final_yelp_data.to_csv(final_data, index=False)


def clean_categories(data: pd.DataFrame):

    # Make the categories column not nasty

    data['categories'] = data['categories'].apply(
                                              lambda x: str(x).lower()
                                            )
    data['categories'] = data['categories'].apply(
                                              lambda x: str(x).replace(',', '')
                                            )
    # Things we dont want

    drop_list = ['veteri', 'pets', 'restaura', 'dent', 'eyewear', 'spas'
                 'glass', 'crafts', 'chiro', 'pharmacy', 'fashion',
                 'diagnostic', 'herbal', 'vape']

    # Get rid of the things

    for i in drop_list:

        data = data[~data['categories'].str.contains(i)]

    data = data.dropna(subset=['compound'])

    return data


if __name__ == '__main__':
    
    subprocess.run(['./bash_scripts/preprocess_location.sh'])    

    bid_contains_doc_json = 's3://trecs-data-s3/data/business_data/yelp_business_contains_doctor.json'
    bid_contains_doc_csv = 's3://trecs-data-s3/data/business_data/yelp_bid_contains_doctor.csv'
    bid_sent = 's3://trecs-data-s3/data/sentiment_data/yelp_bid_review_sentiment.csv'
    
    final_sentiment_data = 's3://trecs-data-s3/data/sentiment_data/final_yelp_sent_data.csv'

    get_bid_contains_doc_csv(bid_contains_doc_json, bid_contains_doc_csv)
    combine_yelp_sent_loc_data(bid_contains_doc_csv, bid_sent, final_sentiment_data)
