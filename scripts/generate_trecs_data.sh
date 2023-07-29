#!/bin/bash

echo Preprocessing yelp data...
/home/ec2-user/miniconda3/bin/python preprocess_yelp_data.py
echo Completed preprocessing data. 

echo Running VADER sentiment analysis...
/home/ec2-user/miniconda3/bin/python yelp_sentiment.py
echo Completed sentiment analysis.

echo Combining sentiment datasets...
/home/ec2-user/miniconda3/bin/python yelp_post_sentiment_combiner.py
echo Done combining datasets.

echo Combining sentiment and location datasets...
/home/ec2-user/miniconda3/bin/python final_data_combiner.py
echo Done combining datasets. 