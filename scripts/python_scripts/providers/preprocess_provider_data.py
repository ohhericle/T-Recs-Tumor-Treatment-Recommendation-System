import uuid
import boto3
import datetime
import pandas as pd


def get_oncologists(medical_providers: str):

    providers = pd.read_csv( 
                             medical_providers, 
                             encoding='unicode_escape', 
                             low_memory=False,
                             converters={"zip": str} 
                           )

    # fix the weird characters in the header :)

    cols_list = list(providers.columns)
    to_rename = cols_list[:2]

    map = {to_rename[0] : 'line',
           to_rename[1] : 'NPI'}

    providers = providers.rename(columns=map)

    # only keep providers that have any level of specialization in oncology
    oncologists = providers[
                    (providers['pri_spec'].str.contains('ONCOLOGY'))   |
                    (providers['sec_spec_1'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_2'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_3'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_4'].str.contains('ONCOLOGY')) |
                    (providers['sec_spec_all'].str.contains('ONCOLOGY'))
                 ]

    current_year = datetime.date.today().year
    oncologists['years_of_experience'] = current_year - oncologists['Grd_yr']
    
    # normalize format of column data 
    oncologists = oncologists.fillna('')

    oncologists['full_name'] = oncologists['lst_nm'] + ', ' + \
                               oncologists['frst_nm'] + ' ' + \
                               oncologists['mid_nm'].replace('', '')
 
    oncologists['full_address'] = oncologists['adr_ln_1'].str.upper() + ' ' + \
                                  oncologists['adr_ln_2'].str.upper() + ' ' + \
                                  oncologists['cty'].str.upper() + ', ' + \
                                  oncologists['st'] + ' ' + \
                                  oncologists['zip'].astype(str)

    oncologists['zip'] = oncologists['zip'].str[:5]
    oncologists = oncologists[oncologists['st'] != 'PR']
    
    oncologists['uuid'] = oncologists.apply(lambda _: uuid.uuid4().hex, axis=1)
    oncologists['uuid'] = oncologists['uuid'].astype(str)


    oncologists.to_csv(
            's3://trecs-data-s3/data/clean_data/oncologists.csv',
            index=False
    )


if __name__ == '__main__':
    
    get_oncologists('s3://trecs-data-s3/data/raw_data/medical_providers.csv') 
