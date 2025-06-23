import pandas as pd
import json

def data(var):
    try:
        with open(f'{var}_info.json', 'r') as f:
            json_data = json.load(f)
            print('data loaded into data')
    except Exception as e:
        print('An error occured: {e}')

    data = pd.DataFrame([json_data])

    # print(data.head())

    col_to_keep = ['Symbol', 'Name', 'Exchange', 'Currency', 'Country', 'Sector', 'Industry']

    data = data[col_to_keep]

    return data

