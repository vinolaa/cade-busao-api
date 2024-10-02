import psycopg2
from psycopg2 import sql


class PostgresRepository:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres",
            password="luck2012",
            host="localhost",
            port="5432",
            database="cade_busao"
        )
        self.engine = self.connection.cursor()

    def execute_query(self, query, params=None, commit=False):
        try:
            self.engine.execute(sql.SQL(query), params)
            if commit:
                self.connection.commit()
            return self.engine
        except Exception as e:
            self.connection.rollback()
            raise e
