from src.agents import BaseAgent, AgentStatus
from abc import abstractmethod
import pandas as pd
import json



class BaseDataTransformer(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name=name, agent_type="Data Transformer")
    # @abstractmethod
    # def transform_data(self, data: dict, name: str):
    #     pass


class AlphaVantageTransformer(BaseDataTransformer):
    def __init__(self, data: dict):
        super().__init__(name="Alpha Vantage")
        self.data = data
        self.processed_data = None

    def transform_company_data(self):

        data = pd.DataFrame([self.data])

        # print(data.head())

        col_to_keep = ['Symbol', 'Name', 'Exchange', 'Currency', 'Country', 'Sector', 'Industry']

        self.processed_data = data[col_to_keep]

        return self.processed_data

    def transform_stock_data(data: dict):
        data = pd.DataFrame([data])
        pass
        