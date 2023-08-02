import pandas as pd


def get_final_oncologist_dataset(in_path: str, out_path: str):

    provider_data = pd.read_csv(
                                 in_path,
                                 encoding='unicode_escape',
                                 converters={"zip": str}
                                )

    # for each NPI: drop rows where place keys are duplicated 
    # AKA only keep unique place keys for each doc

    # get provider data at NPI, go unique on place keys = get uuids

    unique_npis = list(set(provider_data['NPI'].tolist()))
    uuid_placekey_frame = pd.DataFrame(columns = provider_data.columns)

    for npi in unique_npis:
        npi_data = provider_data[provider_data['NPI'] == npi]
        npi_data = npi_data.drop_duplicates(subset=['placekey'])
        uuid_placekey_frame = pd.concat([uuid_placekey_frame, npi_data])
    
    uuid_placekey_frame.to_csv(out_path)


if __name__ == '__main__':
    
    oncologist_data = 's3://trecs-data-s3/data/clean_data/placekey_oncologist_dataset.csv'
    final_oncologist_data = 's3://trecs-data-s3/data/clean_data/final_oncologist_dataset.csv'

    get_final_oncologist_dataset(oncologist_data, final_oncologist_data)
