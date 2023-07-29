#!/bin/bash

YELP_BUS_RAW_DATA=/home/ec2-user/capstone/data/raw_data/yelp_academic_dataset_business.json
YELP_BUS_FILTERED_DATA=/home/ec2-user/capstone/data/business_data/yelp_business_contains_doctor.json
YELP_BUS_CAT=/home/ec2-user/capstone/data/business_data/doctor_categories.txt

if [ -f ${YELP_BUS_FILTERED_DATA} ]; then
	> ${YELP_BUS_FILTERED_DATA}
else
	touch ${YELP_BUS_FILTERED_DATA}  
fi

for i in $( cat ${YELP_BUS_CAT} ); do 
	cat ${YELP_BUS_RAW_DATA} | grep -i $i  >> ${YELP_BUS_FILTERED_DATA} 
done
