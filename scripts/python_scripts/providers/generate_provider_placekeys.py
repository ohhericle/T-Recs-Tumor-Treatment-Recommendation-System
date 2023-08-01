import uuid
import json
import requests
import warnings
import numpy as np
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

    provider_data = pd.read_csv(
                                 in_datapath, 
                                 encoding='unicode_escape',
                                 converters={"zip": str}
                                )

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
    addresses = addresses.fillna(np.nan)
    
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

    predrop_placekeys = placekeys_data['uuid'].tolist()
    placekeys_data = placekeys_data.drop(columns=['error'])
    placekeys_data = placekeys_data.dropna()
    postdrop_placekeys = placekeys_data['uuid'].tolist()

    placekeys_data['placekey'] = placekeys_data['placekey'].apply(lambda x: str(x)[3:-2])

    missing_placekeys = list(set(predrop_placekeys) - set(postdrop_placekeys))

    full_add_placekeys = None
    if len(missing_placekeys) > 0:
        provider_missing_placekeys = provider_data[
                                       provider_data['uuid'].isin(missing_placekeys)
                                     ]
        provider_missing_placekeys = provider_missing_placekeys.drop_duplicates(subset=['uuid'])
        full_add_placekeys = get_full_address_placekeys(provider_missing_placekeys)

    placekeys_data = pd.concat([placekeys_data, full_add_placekeys])


    provider_data_final = provider_data.merge(placekeys_data, on='uuid', how='left')    
    provider_data_final = match_missing_placekeys(provider_data_final)
    provider_data_final = provider_data_final.dropna(subset=['placekey'])

    provider_data_final.to_csv(out_datapath) 


def get_full_address_placekeys(provider_data: pd.DataFrame):
    '''
    Call the placekeys API to get placekeys based on coordinates
    '''
    add_cols = [ 'uuid',
                 'org_nm',
                 'adr_ln_1',
                 'adr_ln_2',
                 'cty',
                 'st',
                 'zip' ]   

    addresses = provider_data[add_cols]
    addresses['iso_country_code'] = 'US'
 
    addresses['address'] = addresses['adr_ln_1'] + ' ' + addresses['adr_ln_2']
    addresses = addresses.drop(columns=['adr_ln_1', 'adr_ln_2'])

    for i in addresses.columns:
        addresses[i] = addresses[i].astype(str)

    new_cols = { 'uuid': 'query_id',
                 'org_nm': 'location_name',
                 'address': 'street_address',
                 'cty': 'city',
                 'st': 'region',
                 'zip': 'postal_code' }

    addresses = addresses.rename(columns=new_cols)
    addresses = addresses.fillna(np.nan)
    
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

    placekeys_data['placekey'] = placekeys_data['placekey'].apply(lambda x: str(x)[str(x).index('@'):-2])

    return placekeys_data


def match_missing_placekeys( placekey_data: pd.DataFrame):
    missing = placekey_data[placekey_data['placekey'].isnull()]
    uuid = missing['uuid'].to_list()
    zip = missing['zip'].to_list()
    orgs = missing['org_nm'].to_list()

    orgs = [str(i) for i in orgs]
    
    provider_map = placekey_data[['org_nm', 'zip', 'placekey']]

    for i,v in enumerate(uuid):

        on_zip = provider_map[provider_map['zip'] == zip[i]]

        if orgs[i] == 'nan':
            continue

        on_org = on_zip[on_zip['org_nm'] == str(orgs[i])]
        
        on_org = on_org.dropna(subset=['placekey'])
        
        if len(on_org) > 0: 
            org_nm = on_org['org_nm'].tolist()[0]
        else:
            continue
        
        placekey = on_org['placekey'].tolist()[0]
    
        index = placekey_data.loc[placekey_data['uuid'] == v].index[0]
        placekey_data.loc[index, 'placekey'] = placekey

    return placekey_data


if __name__ == '__main__':

    provider_data = 's3://trecs-data-s3/data/clean_data/oncologists.csv'
    final_data = 's3://trecs-data-s3/data/clean_data/placekey_oncologist_dataset.csv' 
    
    get_placekeys_address(provider_data, final_data)
