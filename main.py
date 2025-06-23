from src.test import get_data
from src.data_transform import data
from src.db_insert import insert_data
from src.db_connect import get_connection



def main():
    get_data('TSLA')
    x = data('TSLA')
    insert_data(x)

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM companies")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    conn.close()

if __name__ == "__main__":
    main()