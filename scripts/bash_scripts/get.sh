#!/bin/bash

if [ -f /home/ec2-user/capstone/data/raw_data/yelp_bid_name.csv ]; then
	> /home/ec2-user/capstone/data/raw_data/yelp_bid_name.csv
	
else
	touch /home/ec2-user/capstone/data/raw_data/yelp_bid_name.csv 
fi

echo business_id,business_name >> /home/ec2-user/capstone/data/raw_data/yelp_bid_name.csv

for i in $( cat $1 | jq .business_id ); do
	id=$i
	business=$(curl -s https://www.yelp.com/biz/$(echo ${i} | sed -e 's/\"//g') | grep -v https: | grep /biz/ | sed -e 's/\/biz\///g' | cut -d' ' -f7 )
	echo $id,$business >> /home/ec2-user/capstone/data/raw_data/yelp_bid_name.csv
done
