#!/bin/bash
set -x


function copy_to_aws(){
	aws s3 cp $1 s3://trecs-data-s3/data/raw_data/
}


mkdir -p temp_data/raw_data
mkdir -p temp_data/clean_data
aws s3 cp s3://trecs-data-s3/data/raw_data/yelp_academic_dataset_review.json temp_data/raw_data
aws s3 cp s3://trecs-data-s3/data/raw_data/medical_terms.txt temp_data/raw_data

RAW_DATA=temp_data/raw_data/yelp_academic_dataset_review.json
MEDICAL_TERMS=temp_data/raw_data/medical_terms.txt

# Create yelp_contains_doctor.json
DOCTOR_DATA=temp_data/raw_data/yelp_contains_doctor.json
touch ${DOCTOR_DATA}
for i in $( cat ${MEDICAL_TERMS} ); do
	cat ${RAW_DATA} | grep -i $i  >> ${DOCTOR_DATA}
done

# Grep out the things that we do not want in the data

copy_to_aws $DOCTOR_DATA
