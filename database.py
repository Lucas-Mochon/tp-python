import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        print("Erreur de connexion PostgreSQL")
        print(e)
        return None
