#!/bin/bash


for i in $( ls /home/ec2-user/capstone/data/yelp_business_ids_dir | grep output ); do

	./get.sh /home/ec2-user/capstone/data/yelp_business_ids_dir/$i &
done

wait
echo Done
