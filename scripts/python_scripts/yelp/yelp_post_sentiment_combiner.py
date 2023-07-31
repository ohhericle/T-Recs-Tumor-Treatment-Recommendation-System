import os
import boto3
import pandas as pd


def combine_bid_sent(bid_rev_sent: str):

    data = pd.read_csv(bid_rev_sent)
    data = data[
        ['business_id', 'positive', 'negative', 'neutral', 'compound']
    ]

    data = data.groupby('business_id').mean().reset_index()
    data = pd.DataFrame(data)
    
    data.to_csv('s3://trecs-data-s3/data/sentiment_data/yelp_bid_sent.csv', index=False)


def combine_bid_sent_name(rev_sent_path: str, bid_name_path: str): 

    rev_sent = pd.read_csv(rev_sent_path)
    bid_name = pd.read_csv(bid_name_path)

    bids = bid_name['business_id'].to_list()
    names = bid_name['business_name'].to_list()

    mapping = {}

    for i, v in enumerate(bids):
        mapping[v] = names[i]

        rev_sent['positive'] = rev_sent['positive'].astype(str)
        rev_sent['negative'] = rev_sent['negative'].astype(str)
        rev_sent['neutral'] = rev_sent['neutral'].astype(str)
        rev_sent['compound'] = rev_sent['compound'].astype(str)

    rev_sent['business_name'] = rev_sent['business_id'].apply(
            lambda x: mapping[x]
    )

    rev_sent.to_csv(
        's3://trecs-data-s3/data/sentiment_data/yelp_bid_sent_name.csv', index=False
    )


if __name__ == '__main__':

    bid_review_sent = 's3://trecs-data-s3/data/sentiment_data/yelp_bid_review_sentiment.csv'
    

    combine_bid_sent(bid_review_sent)

    rev_sent_path = 's3://trecs-data-s3/data/sentiment_data/yelp_bid_sent.csv'
    bid_name_path = 's3://trecs-data-s3/data/processed_raw_data/yelp_bid_name.csv'

    combine_bid_sent_name(rev_sent_path, bid_name_path)
