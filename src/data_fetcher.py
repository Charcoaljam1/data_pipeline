from src.agents import BaseAgent, AgentStatus
import requests 
import json
import yaml
from abc import abstractmethod
from typing import Optional

# What every fetcher MUST do
class BaseDataFetcher(BaseAgent):
    def __init__(self, name: str, agent_type: str ):
        super().__init__(name=name, agent_type=agent_type)
    @abstractmethod
    def get_data(self):
        """
        Abstract method to fetch data.
        Concrete implementations must provide data for the given symbols and functions.
        """
        pass

class APIDataFetcher(BaseDataFetcher):
    def __init__(self, name: str, url: str, api_key: str):
        super().__init__(name,agent_type="API Data Fetcher")
        self.url = url
        self._api_key = api_key

    
class AlphaVantageFetcher(APIDataFetcher):
    def __init__(self, url: str, api_key: str, symbols: list, functions: list, function_mapping: dict, output_size: str = "full"):
        super().__init__(name="Alpha Vantage", url=url, api_key=api_key)
        self.symbols = symbols
        self.functions = functions
        self.map = function_mapping
        self.size = output_size

        # Internal mapping from function names to internal helper methods
        self._internal_method_map = {
            "time_series_daily":  self._get_stock_data,
            "company_overview": self._get_company_data,
            "income_statement": self._get_income_data,
            "balance_sheet":self._get_balance_sheet_data,
            "cash_flow": self._get_cash_flow_data
        }

    def _make_request(self,function: str, symbol: str, output_size: Optional[str] = None) -> dict:
        """
        Helper to make the API call. This is placed here as it's specific to Alpha Vantage
        response patterns (e.g., "Error Message", "Note").
        """
        parameters = {'function': function, 'symbol':symbol, 'apikey': self._api_key}
        
        if output_size:
            parameters.update({'outputsize':output_size})

        response = requests.get(url=self.url, params=parameters)

        if response.status_code == 200:
            return response.json()

    
    def _get_stock_data(self, symbols: list) -> dict:

        data = {}
        for symbol in symbols:
            data[symbol] = self._make_request(self.map['time_series_daily'], symbol, self.size)
            
        return data

    def _get_company_data(self, symbols: list) -> dict:

        data = {}
        for symbol in symbols:
            data[symbol] = self._make_request(self.map['company_overview'], symbol)
                        
        return data

    def _get_income_data(self, symbols: list) -> dict:

        data = {}
        for symbol in symbols:
            data[symbol] = self._make_request(self.map['income_statement'], symbol)
            
        return data
        
    def _get_balance_sheet_data(self, symbols: list) -> dict:

        data = {}
        for symbol in symbols:
            data[symbol] = self._make_request(self.map['balance_sheet'], symbol)
            
        return data
        
    def _get_cash_flow_data(self, symbols: list) -> dict:

        data = {}
        for symbol in symbols:
            data[symbol] = self._make_request(self.map['cash_flow'], symbol)
            
        return data
    
    def get_data(self) -> dict:
        
        self.set_status(AgentStatus.BUSY)
        fetched_data_by_function = {}
        
        for function in self.functions:
            fetched_data_by_function[function] = self._internal_method_map[function](self.symbols)

        return fetched_data_by_function
    


            

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


