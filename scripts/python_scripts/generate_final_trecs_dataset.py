import math
import boto3
import numpy as np
import pandas as pd




def generate_trecs_dataset( 
                            yelp_path: str, 
                            onc_path: str, 
                            zip_pk_path: str,
                            final_trecs_data_path: str
                          ):

    yelp_data = pd.read_csv(yelp_path)
    oncologist_data = pd.read_csv( 
                                   onc_path,
                                   encoding='unicode_escape',
                                   converters={'zip': str}
                                 )

    zip_code_placekeys = pd.read_csv(zip_pk_path, converters={'zip': str})


    trecs_data = pd.merge(oncologist_data, yelp_data, on='placekey', how='left')
    trecs_data = trecs_data.drop_duplicates(subset=['uuid'])

    org_mean_compounds = trecs_data.groupby('org_nm')['compound'].mean().to_dict()

    def get_missing_scores(row):
        if np.isnan(row['compound']):
            return org_mean_compounds.get(row['org_nm'], np.NaN)
        return row['compound']

    trecs_data['compound'] = trecs_data.apply(get_missing_scores, axis=1)


    zip_code_placekeys= zip_code_placekeys.rename(columns={
                                                     'placekey': 'Centroid Placekey',
                                                     'latitude': 'Centroid Latitude',
                                                     'longitude': 'Centroid Longitude'
                                                })

    trecs_data = trecs_data.merge(zip_code_placekeys, on='zip', how='left')

    trecs_data = trecs_data [[  
                                'uuid', 
                                'full_name', 
                                'gndr', 
                                'Cred', 
                                'years_of_experience', 
                                'Med_sch',
                                'org_nm', 
                                'full_address', 'phn_numbr', 
                                'cty', 
                                'zip', 
                                'compound', 
                                'placekey', 
                                'Centroid Placekey', 
                                'Centroid Latitude', 
                                'Centroid Longitude' 
                            ]]

    new_columns = {
        'full_name': 'Oncologist Name',
        'gndr': 'Gender',
        'Cred': 'Credential',
        'years_of_experience': 'Years of Experience',
        'Med_sch': 'Medical School',
        'org_nm': 'Org Name',
        'full_address': 'Address',
        'phn_numbr': 'Phone Number',
        'cty': 'City',
        'zip': 'Zip',
        'compound': 'Overall Score',
        'placekey': 'Org Placekey'
    }

    trecs_data = trecs_data.rename(columns=new_columns)

    trecs_data.to_csv(final_trecs_data_path)


if __name__ == '__main__':

    yelp_data = 's3://trecs-data-s3/data/clean_data/final_yelp_dataset.csv'
    onc_data = 's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv'
    zip_pks = 's3://trecs-data-s3/data/raw_data/zip_centroid_placekey.csv'
    final_data_path = 's3://trecs-data-s3/data/final/trecs.csv'

    generate_trecs_dataset(yelp_data, onc_data, zip_pks, final_data_path)
