#!/bin/bash

RAW_DATA=/home/ec2-user/capstone/data/raw_data/yelp_academic_dataset_review.json
DOCTOR_DATA=/home/ec2-user/capstone/data/raw_data/yelp_contains_doctor.json
BID=/home/ec2-user/capstone/data/raw_data/yelp_bid.csv
TEXT=/home/ec2-user/capstone/data/raw_data/yelp_review_text.txt

# Create /home/ec2-user/capstone/data/raw_data/yelp_contains_doctor.json

if [ -f ${DOCTOR_DATA} ]; then
	> ${DOCTOR_DATA}
else
	touch ${DOCTOR_DATA}

fi

cat ${RAW_DATA} | grep -i 'doctor' >> ${DOCTOR_DATA}


# Create /home/ec2-user/capstone/data/raw_data/yelp_bid.csv

if [ -f ${BID} ]; then
	> ${BID}

else 
	touch ${BID}

fi

echo "business_id" >> ${BID}

cat ${DOCTOR_DATA} | jq .business_id >> ${BID}

# Create /home/ec2-user/capstone/data/raw_data/yelp_review_text.txt

if [ -f ${TEXT} ]; then
	> ${TEXT}

else 
	touch ${TEXT}

fi

cat ${DOCTOR_DATA} | jq .text >> ${TEXT}
