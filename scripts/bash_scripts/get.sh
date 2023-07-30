#!/bin/bash
set -x

touch temp_data/processed_raw_data/yelp_bid_name.csv 
echo business_id,business_name >> temp_data/processed_raw_data/yelp_bid_name.csv

for i in $( cat $1 | jq .business_id ); do
	id=$i
	business=$(curl -s https://www.yelp.com/biz/$(echo ${i} | sed -e 's/\"//g') | grep -v https: | grep /biz/ | sed -e 's/\/biz\///g' | cut -d' ' -f7 )
	echo $id,$business >> temp_data/processed_raw_data/yelp_bid_name.csv
done
