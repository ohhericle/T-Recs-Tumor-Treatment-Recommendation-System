#!/bin/bash
set -x


function copy_to_aws(){
	aws s3 cp $1 s3://trecs-data-s3/data/processed_raw_data/
}


mkdir -p temp_data/raw_data
mkdir -p temp_data/processed_raw_data
aws s3 cp s3://trecs-data-s3/data/raw_data/yelp_academic_dataset_review.json temp_data/raw_data
aws s3 cp s3://trecs-data-s3/data/raw_data/doctor_categories.txt temp_data/raw_data

RAW_DATA=temp_data/raw_data/yelp_academic_dataset_review.json
MEDICAL_TERMS=temp_data/raw_data/doctor_categories.txt


# Create yelp_contains_doctor.json
DOCTOR_DATA=temp_data/processed_raw_data/yelp_contains_doctor.json
for i in $( cat ${MEDICAL_TERMS} ); do
	cat ${RAW_DATA} | grep -i $i  >> ${DOCTOR_DATA}
done

# Create yelp_bid.csv
BID=temp_data/processed_raw_data/yelp_bid.csv
touch ${BID}
echo "business_id" >> ${BID}
cat ${DOCTOR_DATA} | jq .business_id >> ${BID}


# Create yelp_review_text.txt
TEXT=temp_data/processed_raw_data/yelp_review_text.txt
touch ${TEXT}
cat ${DOCTOR_DATA} | jq .text >> ${TEXT}


copy_to_aws $DOCTOR_DATA
copy_to_aws $BID 
copy_to_aws $TEXT 
