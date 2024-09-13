import os
import psycopg2
from psycopg2 import sql
import logging
logging.basicConfig(level=logging.INFO)
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ['PGHOST'],
            database=os.environ['PGDATABASE'],
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            port=os.environ['PGPORT']
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None
def create_mailwizz_connections_table():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mailwizz_connections (
                    id SERIAL PRIMARY KEY,
                    instance_name TEXT NOT NULL UNIQUE,
                    api_url TEXT NOT NULL,
                    public_key TEXT NOT NULL,
                    secret_key TEXT NOT NULL,
                    list_id TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info("mailwizz_connections table created successfully")
    except Exception as e:
        logging.error(f"Error creating mailwizz_connections table: {e}")
    finally:
        conn.close()
if __name__ == "__main__":
    create_mailwizz_connections_table()