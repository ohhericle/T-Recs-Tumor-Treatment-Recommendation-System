import pandas as pd


def clean_categories(data: pd.DataFrame):

    data = pd.read_csv(data)

    # Make the categories column not nasty

    data['categories'] = data['categories'].apply(lambda x: str(x).lower())
    data['categories'] = data['categories'].apply(lambda x: str(x).replace(',', ''))


    # Things we dont want

    drop_list = ['veteri', 'pets', 'restaura', 'dent', 'eyewear', 'spas'
                 'glass', 'crafts', 'chiro', 'pharmacy', 'fashion',
                 'diagnostic', 'herbal', 'vape']

    # Get rid of the things

    for i in drop_list:

        data = data[~data['categories'].str.contains(i)]


    data = data.dropna(subset=['compound'])

    data.to_csv('filtered.csv', index=False)


if __name__ == '__main__':

    clean_categories('test_data.csv')
