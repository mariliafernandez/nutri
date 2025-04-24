import mysql.connector
from typing import Literal
from src.QueryFactory import QueryFactory


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(
        self,
        host: str = "127.0.0.1",
        port: int = 3306,
        user: str = "root",
        password: str = "admin",
    ):
        # Simulate a database connection
        self.connection = mysql.connector.connect(
            database=self.db_name, host=host, port=port, user=user, password=password
        )

    def disconnect(self):
        # Simulate closing the database connection
        self.connection.close()

    def find_subtring(self, substring: str):
        if self.connection:
            query = "SELECT * FROM taco WHERE description LIKE %s"
            query = query % f"'%{substring}%'"
            print(f"Executed query: {query}")
            cur = self.connection.cursor(dictionary=True)
            cur.execute(query)
            result = cur.fetchall()
            return result
        else:
            print("No connection to the database.")
            return None

    def insert(self, table_name, data_list):
        if self.connection:
            cur = self.connection.cursor()
            columns = ", ".join(data_list[0].keys())
            values = ", ".join(["%s"] * len(data_list[0]))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            print(sql)
            if len(data_list) > 1:
                cur.executemany(sql, [tuple(data.values()) for data in data_list])
                print(cur.statement)
            else:
                cur.execute(sql, tuple(data_list[0].values()))
            self.connection.commit()
            print(f"Inserted rows into {table_name}.")
        else:
            print("No connection to the database.")

    def select(
        self,
        table_name,
        columns="*",
        description_like: str = None,
        categories: list = [],
        id: int = None,
        order_by: str = "",
        order: Literal["ASC", "DESC"] = "ASC",
        limit: int = None,
    ):
        conditions = []
        if description_like is not None:
            conditions.append({"description": description_like})
        if id is not None:
            conditions.append({"id": id})
        if categories != []:
            conditions.append({"category": categories})

        query_factory = QueryFactory(
            table_name=table_name,
            columns=columns,
            where_conditions=conditions,
            order_by=order_by,
            order=order,
            limit=limit,
        )
        query_factory.make_select()

        with self.connection.cursor(dictionary=True) as cursor:
            print("Executing query:", query_factory.query)
            cursor.execute(query_factory.query)
            result = cursor.fetchall()
            return result
