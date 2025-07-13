import requests 
import json
import yaml

with open('alpha_vantage.yaml','r') as f:
    config = yaml.safe_load(f)

url = config['api_settings']['base_url']
function = config['api_function_mapping']['time_series_daily']
size = config['api_settings']['default_output_size']
symbols = config['tickers']['second']

def get_data(symbols: list|str)->dict:
    """Fetches stock data from Alpha Vantage API for given symbols."""

    for symbol in symbols:
        response = requests.get(url=url, 
                                params={f'function': function, 'symbol':symbol, 'apikey':'WWNHUP2UL6ATA8QA', 'outputsize':'full'})


        try: 
            # This line needs to be configurable and dynamic as the  temporary storage path can change at any time. Thus, this line won't be hardcoded
            with open(f'{symbol}_{function}.json', 'w') as f:
                json.dump(response.json(),f, indent=4)
                print('api_data.json created successfully')
        except Exception as e:
            print(f'Error writing to file: {e}')


