import os
import psycopg
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

HOST = os.environ.get("DB_HOST", "localhost")
DATABASE = os.environ.get("DB_NAME", "movie_recommender")
USER = os.environ.get("DB_USER", None)
PASSWORD = os.environ.get("DB_PASSWORD", None)
PORT = os.environ.get("DB_PORT", 5432)

if USER is None:
    raise RuntimeError("database user is not provided")

if PASSWORD is None:
    raise RuntimeError("database password is not provided")

connection_params = {
    "host": HOST,
    "dbname": DATABASE,
    "user": USER,
    "password": PASSWORD,
    "port": PORT,
}

@contextmanager
def connect():
    with psycopg.connect(**connection_params) as conn:
        yield conn