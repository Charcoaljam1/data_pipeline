# from src.test import get_data
from src.data_transform import AlphaVantageTransformer
from src.db_insert import insert_data
from src.db_connect import get_connection
from src.data_fetcher import AlphaVantageFetcher
import os
from dotenv import load_dotenv
from src.data_saver import JSONFileSaver
from src.utils import open_json
from pathlib import Path 



def main():
   

    load_dotenv()

    map = {
            'time_series_daily': "TIME_SERIES_DAILY",
            'company_overview': "OVERVIEW",
            'income_statement': "INCOME_STATEMENT",
            'balance_sheet': "BALANCE_SHEET",
            'cash_flow': "CASH_FLOW"
    }
    API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

    fetcher = AlphaVantageFetcher('https://www.alphavantage.co/query', 'demo',['IBM'],['company_overview'], map)
    ibm = fetcher.get_data()
    json_save = JSONFileSaver(output_directory=Path('data/raw_json/'))
    json_save.save_data(ibm)

    data = open_json(filepath=Path('data/raw_json/IBM_company_overview.json'))
    transform = AlphaVantageTransformer(data)
    transform.transform_company_data()


    insert_data(transform.processed_data)

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM companies")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    conn.close()

if __name__ == "__main__":
    main()