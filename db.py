from sqlite3 import Cursor
from psycopg2.pool import ThreadedConnectionPool, SimpleConnectionPool
from psycopg2.extras import RealDictCursor
import dotenv
from os import getenv

from pydantic import BaseModel

dotenv.load_dotenv()


class DbConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str


class DbConfigBuilder():
    def from_env():
        return DbConfig(host=getenv("DB_HOST"), user=getenv("DB_USER"),
                        password=getenv("DB_PASSWORD"), database=getenv("DB_NAME"))


class DbPoolFactory:
    def create_threaded_pool(conf: DbConfig = DbConfigBuilder.from_env()):
        return ThreadedConnectionPool(1, 5,
                                      user=getenv("DB_USER"),
                                      host=getenv("DB_HOST"),
                                      password=getenv("DB_PASSWORD"),
                                      database=getenv("DB_NAME"),)

    def create_simple_pool(conf: DbConfig = DbConfigBuilder.from_env()):
        return SimpleConnectionPool(1, 5,
                                    user=getenv("DB_USER"),
                                    host=getenv("DB_HOST"),
                                    password=getenv("DB_PASSWORD"),
                                    database=getenv("DB_NAME"),)


class DatabaseConnection:
    instance = None

    def __init__(self, db_pool: ThreadedConnectionPool) -> None:
        self.db_pool = db_pool

    def get_instance():
        if DatabaseConnection.instance != None:
            return DatabaseConnection.instance
        else:
            db_pool = DbPoolFactory.create_threaded_pool()

        if (db_pool):
            print("Connected to database.")
        else:
            print("Failed to connect to database.")
            raise Exception()

        return DatabaseConnection(db_pool)

    def get_dict_cursor(self) -> RealDictCursor:
        connection = self.db_pool.getconn()
        connection.autocommit = True
        return connection.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query: str, params: any) -> any:
        connection = self.db_pool.getconn()
        connection.autocommit = True

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()

        self.db_pool.putconn(connection)

        return result
