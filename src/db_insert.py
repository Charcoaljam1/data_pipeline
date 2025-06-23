import psycopg2
from src.db_connect import get_connection
# from data_transform import data

conn = get_connection()

def insert_data(data):
    with conn.cursor() as cur:
        for a, b in data.iterrows():
            cur.execute(
                """
                INSERT INTO companies (symbol, company_name, exchange, currency, country, sector, industry)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                tuple(b)
            )
            print("data succesfully inserted")
    conn.commit()
    conn.close()

