import uuid
import json
import requests
import pandas as pd
import placekey as pk
from placekey.api import PlacekeyAPI


with open('../api_key.txt') as f:
    placekey_api_key = f.readline().strip()

pk_api = PlacekeyAPI(placekey_api_key)

def get_placekeys_coords(in_data: str, out_datapath: str):

    '''
    Call the placekeys API to get placekeys based on coordinates
    '''

    yelp_data = pd.read_csv(in_data)
    coordinates = yelp_data.drop_duplicates(subset=['business_id'])
 
    coordinates = coordinates[['business_id', 'latitude', 'longitude']]
    
    coordinates = coordinates.rename(columns={'business_id': 'query_id'})
    coordinates['latitude'] = coordinates['latitude'].astype(float)
    coordinates['longitude'] = coordinates['longitude'].astype(float)

    add_json = json.loads(coordinates.to_json(orient="records"))
    placekeys_output = pk_api.lookup_placekeys(
                            add_json,
                            strict_address_match=False,
                            strict_name_match=False,
                            verbose=True
                       )

    placekeys_data = pd.read_json(
            json.dumps(placekeys_output), dtype={'query_id':str}
            )
    
    
    placekeys_data = placekeys_data.rename(columns={'query_id': 'business_id'})
    placekeys_data['placekey'] = placekeys_data['placekey'].apply(lambda x: x[:-1])
    
    yelp_data_final = yelp_data.merge(placekeys_data, on='business_id')
    yelp_data_final.to_csv(out_datapath) 


if __name__ == '__main__':

    yelp_data = 's3://trecs-data-s3/data/sentiment_data/final_yelp_sent_data.csv'
    final_data = 's3://trecs-data-s3/data/clean_data/final_yelp_dataset.csv' 

    get_placekeys_coords(yelp_data, final_data)
