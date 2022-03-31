from sqlite3 import Cursor
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import dotenv
from os import getenv

dotenv.load_dotenv()

db_pool = ThreadedConnectionPool(1, 5,
                                 user=getenv("DB_USER"),
                                 host=getenv("DB_HOST"),
                                 password=getenv("DB_PASSWORD"),
                                 database=getenv("DB_NAME"),)

if (db_pool):
    print("Connected to database.")
else:
    print("Failed to connect to database.")
    raise Exception()


def get_dict_cursor() -> RealDictCursor:
    connection = db_pool.getconn()
    connection.autocommit = True
    return connection.cursor(cursor_factory=RealDictCursor)
