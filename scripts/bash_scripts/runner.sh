#!/bin/bash
set -x

for i in $( ls temp_data/processed_raw_data/yelp_business_ids_dir | grep output ); do

	./bash_scripts/get.sh temp_data/processed_raw_data/yelp_business_ids_dir/$i &
done

wait
echo Done

aws s3 cp temp_data/processed_raw_data/yelp_bid_name.csv s3://trecs-data-s3/data/processed_raw_data/
rm -rf temp_data
