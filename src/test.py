import requests 
import json

def get_data(x):
    response = requests.get(url='https://www.alphavantage.co/query?', 
                            params={f'function': 'OVERVIEW', 'symbol':{x}, 'apikey':'WWNHUP2UL6ATA8QA', 'outputsize':'full'})

    # print(response.status_code)
    # print(response.json())

    try: 
        with open(f'{x}_info.json', 'w') as f:
            json.dump(response.json(),f, indent=4)
            print('api_data.json created successfully')
    except Exception as e:
        print(f'Error writing to file: {e}')


from pydantic import BaseModel, ConfigDict, Field

class StockPrice(BaseModel):
    open_price: float = Field(gt=0, alias="1. open")
    high_price: float = Field(gt=0, alias="2. high")
    low_price: float = Field(gt=0, alias="3. low")
    close_price: float = Field(gt=0, alias="4. close")
    volume: int = Field(ge=0, alias="5. volume")

    model_config = ConfigDict(populate_by_name=True)

class MetaData(BaseModel):
    info: str = Field(alias= "1. Information")
    symbol: str = Field(alias = "2. Symbol")
    refresh_date: str = Field(alias = "3. Last Refreshed")
    output_size: str = Field(alias = "4. Output Size")
    time_zone: str = Field(alias = "5. Time Zone")

    model_config = ConfigDict(populate_by_name=True)

class Data(BaseModel):
    metadata: MetaData = Field(alias = "Meta Data")
    time_series: dict[str, StockPrice] = Field(alias = "Time Series (Daily)")

    model_config = ConfigDict(populate_by_name=True)


# try:
#     with open('raw_MSFT.json', 'r') as f:
#         data = f.read()
#         print('api_data rread.')

# except Exception as e:
#     print(e)

# m=Data.model_validate_json(data)
# print(dir(m))


# df = []

# for date, stock in m.time_series.items():
#     df.append({
#         'date': date,
#         'high_price': stock.high_price,
#         'close_price': stock.close_price,
#         'volume': stock.volume
#     })

# print(df)

# import pandas as pd
# df = pd.DataFrame(df)

# print(df.head())
# print(m.metadata)