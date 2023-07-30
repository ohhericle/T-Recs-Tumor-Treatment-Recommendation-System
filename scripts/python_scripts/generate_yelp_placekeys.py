import uuid
import json
import requests
import pandas as pd
import placekey as pk
from placekey.api import PlacekeyAPI


with open('../api_key.txt') as f:
    placekey_api_key = f.readline().strip()

pk_api = PlacekeyAPI(placekey_api_key)

def get_placekeys_address(in_datapath: str, out_datapath: str):

    '''
    Call the placekeys api to get the placekeys based
    on the address in the dataframe
    '''

    yelp_data = pd.read_csv(in_datapath)
    addresses = yelp_data.drop_duplicates(subset=['business_id'])
    
    add_cols = [ 'business_id',
                 'name',
                 'address', 
                 'city', 
                 'state', 
                 'postal_code' ]
    
    addresses = addresses[add_cols]
    addresses['iso_country_code'] = 'US'
    
    for i in addresses.columns:
        addresses[i] = addresses[i].astype(str)
    
    new_cols = { 'business_id': 'query_id',
                 'name': 'location_name',
                 'address': 'street_address',
                 'city': 'city',
                 'state': 'region',
                 'postal_code': 'postal_code' }
    addresses = addresses.rename(columns=new_cols)
    
    
    add_json = json.loads(addresses.to_json(orient="records"))
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
    
    predrop_placekeys = placekeys_data['business_id'].tolist()
    
    placekeys_data = placekeys_data.drop(columns=['error'])
    placekeys_data = placekeys_data.dropna()
    
    postdrop_placekeys = placekeys_data['business_id'].tolist()

    missing_placekeys = list(set(predrop_placekeys) - set(postdrop_placekeys))
    
    coordinate_placekeys = None
    if len(missing_placekeys) > 0:

        yelp_missing_placekeys = yelp_data[
                                   yelp_data['business_id'].isin(missing_placekeys)
                                 ]

        yelp_missing_placekeys = yelp_missing_placekeys.drop_duplicates(subset=['business_id'])
        coordinate_placekeys = get_placekeys_coords(yelp_missing_placekeys)

    placekeys_data = pd.concat([placekeys_data, coordinate_placekeys])
    
    yelp_data_final = yelp_data.merge(placekeys_data, on='business_id')
    
    yelp_data_final.to_csv(out_datapath) 

def get_placekeys_coords(data: pd.DataFrame):

    '''
    Call the placekeys API to get placekeys based on coordinates
    '''

    coordinates = data[['business_id', 'latitude', 'longitude']]
    
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
    
    return placekeys_data


if __name__ == '__main__':

    yelp_data = 's3://trecs-data-s3/data/sentiment_data/final_yelp_sent_data.csv'
    final_data = 's3://trecs-data-s3/data/final/final_yelp_dataset.csv' 
    get_placekeys_address(yelp_data, final_data)
