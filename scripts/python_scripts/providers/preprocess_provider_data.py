import uuid
import boto3
import pandas as pd


def get_oncologists(medical_providers: str):
    providers = pd.read_csv(medical_providers, encoding='unicode_escape', low_memory=False)

    # only keep providers that have any level of specialization in oncology
    oncologists = providers[
                    (providers['pri_spec'].str.contains('ONCOLOGY'))   |
                    (providers['sec_spec_1'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_2'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_3'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_4'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_all'].str.contains('ONCOLOGY'))
                 ]

    # normalize format of column data 
    oncologists = oncologists.fillna('')

    oncologists['full_name'] = oncologists['lst_nm'] + ', ' + \
                               oncologists['frst_nm'] + ' ' + \
                               oncologists['mid_nm'].replace('', '')
 
    oncologists['zip'] = oncologists['zip'].str[:5]
    oncologists['zip'] = oncologists['zip'].apply(lambda x: x.zfill(5)).astype(int)

    oncologists['phn_numbr'] = oncologists['phn_numbr'].replace('', 'missing')
    
    # drop duplicates
    oncologists = oncologists.drop_duplicates(subset='full_name', keep='first')
    
    oncologists['uuid'] = oncologists.apply(lambda _: uuid.uuid4().hex, axis=1)
    oncologists['uuid'] = oncologists['uuid'].astype(str)
   
    oncologists.to_csv(
            's3://trecs-data-s3/data/clean_data/oncologists.csv',
            index=False
    )


if __name__ == '__main__':
    
    get_oncologists('s3://trecs-data-s3/data/raw_data/medical_providers.csv') 
