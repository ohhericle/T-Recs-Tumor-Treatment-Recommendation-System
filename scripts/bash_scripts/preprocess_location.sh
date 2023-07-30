#!/bin/bash
set -x

mkdir -p temp_data/raw_data
mkdir -p temp_data/business_data

function copy_from_aws(){
	aws s3 cp s3://trecs-data-s3/data/raw_data/$1 temp_data/raw_data
}


copy_from_aws yelp_academic_dataset_business.json
copy_from_aws doctor_categories.txt 


YELP_BUS_RAW_DATA=temp_data/raw_data/yelp_academic_dataset_business.json
YELP_BUS_CAT=temp_data/raw_data/doctor_categories.txt
YELP_BUS_FILTERED_DATA=temp_data/business_data/yelp_business_contains_doctor.json


touch ${YELP_BUS_FILTERED_DATA}  

for i in $( cat ${YELP_BUS_CAT} ); do 
	cat ${YELP_BUS_RAW_DATA} | grep -i $i  >> ${YELP_BUS_FILTERED_DATA} 
done


aws s3 cp ${YELP_BUS_FILTERED_DATA} s3://trecs-data-s3/data/business_data/
