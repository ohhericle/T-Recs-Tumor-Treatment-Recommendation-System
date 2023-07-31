import uuid
import json
import requests
import warnings
import pandas as pd
import placekey as pk
from placekey.api import PlacekeyAPI

warnings.filterwarnings('ignore')

with open('../api_key.txt') as f:
    placekey_api_key = f.readline().strip()

pk_api = PlacekeyAPI(placekey_api_key)

def get_placekeys_address(in_datapath: str, out_datapath: str):

    '''
    Call the placekeys api to get the placekeys based
    on the address in the dataframe
    '''

    provider_data = pd.read_csv(in_datapath, encoding='unicode_escape')
    
    add_cols = [ 'uuid',
                 'adr_ln_1',
                 'cty', 
                 'st', 
                 'zip' ]
    
    addresses = provider_data[add_cols]
    addresses['iso_country_code'] = 'US'
 
    for i in addresses.columns:
        addresses[i] = addresses[i].astype(str)

    new_cols = { 'uuid': 'query_id',
                 'adr_ln_1': 'street_address',
                 'cty': 'city',
                 'st': 'region',
                 'zip': 'postal_code' }
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
    
    
    placekeys_data = placekeys_data.rename(columns={'query_id': 'uuid'})
    placekeys_data = placekeys_data.drop(columns=['error'])
    placekeys_data = placekeys_data.dropna()
    
    placekeys_data['placekey'] = placekeys_data['placekey'].apply(lambda x: x[3:-2])

    provider_data_final = provider_data.merge(placekeys_data, on='uuid')
    
    provider_data_final.to_csv(out_datapath) 


if __name__ == '__main__':

    provider_data = 's3://trecs-data-s3/data/clean_data/oncologists.csv'
    final_data = 's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv' 
    get_placekeys_address(provider_data, final_data)
