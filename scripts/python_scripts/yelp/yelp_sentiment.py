import boto3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def calculate_sentiment(datapath: str, outfile_path: str):

    '''
    Get all the sentiment scores for the final preprocessed dataset

    input
        yelp_bid_reviews.csv

    output
        yelp_bid_review_sentiment.csv       
    '''

    def _get_sentiment(text: str):
    
        '''
        Function that takes in a string and runs it through VADER
        
        input
            string
    
        output
            sentiment dictionary
        '''
    
        sid_obj = SentimentIntensityAnalyzer()
    
        sentiment_dict = sid_obj.polarity_scores(text)
    
        print(sentiment_dict)
        return sentiment_dict

    dataset = pd.read_csv(datapath)
    
    positive = []
    negative = []
    neutral = []
    compound = []

    for i in dataset['review'].to_list():
        obj = _get_sentiment(i)
        positive.append(obj['pos'])
        negative.append(obj['neg'])
        neutral.append(obj['neu'])
        compound.append(obj['compound'])
    
    dataset['positive'] = positive
    dataset['negative'] = negative
    dataset['neutral'] = neutral
    dataset['compound'] = compound

    dataset = dataset.drop(columns=['review'])
    
    dataset = apply_avg_sent_to_bid(dataset)

    dataset.to_csv(outfile_path, index=False)


def apply_avg_sent_to_bid(data: pd.DataFrame):

    data = data[
        ['business_id', 'positive', 'negative', 'neutral', 'compound']
    ]

    data = data.groupby('business_id').mean().reset_index()
    data = pd.DataFrame(data)

    return data


if __name__ == '__main__':

    
    yelp_bid_rev = 's3://trecs-data-s3/data/clean_data/yelp_bid_reviews.csv'
    bid_review_sent = 's3://trecs-data-s3/data/sentiment_data/yelp_bid_review_sentiment.csv'
    
    calculate_sentiment(yelp_bid_rev, bid_review_sent)





