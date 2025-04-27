import mysql.connector
from typing import Literal
from src.QueryFactory import QueryFactory


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
    ):
        # Simulate a database connection
        self.connection = mysql.connector.connect(
            database=self.db_name, host=host, port=port, user=user, password=password
        )
        print(f"Connected to database {self.db_name} at {host}:{port}")

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
        order_by: str = None,
        order: Literal["ASC", "DESC"] = "ASC",
        limit: int = None,
        distinct: bool = False,
    ):
        conditions = []
        if description_like is not None:
            conditions.append({"description": description_like})
        if id is not None:
            conditions.append({"id": id})
        if categories != []:
            conditions.append({"category": categories})

        qf = QueryFactory(
            table_name=table_name,
            columns=columns,
            where_conditions=conditions,
            order_by=order_by,
            order=order,
            limit=limit,
            distinct=distinct,
        )
        qf.make_select()
        return self.run_query(qf.query)

    def select_relation(
        self,
        table_name: str,
        select_columns: str,
        col1: str,
        col2: str,
        categories: list = [],
        order: str = "DESC",
        limit: int = None,
    ):
        """
        Selects a relation between two columns, avoiding division by zero.
        """

        select_columns += f", {col1} / NULLIF({col2}, 0) AS relation_value"
        where_conditions = [f"{col1} IS NOT NULL", f"{col2} IS NOT NULL"]
        
        if categories != []:
            where_conditions.append({"category": categories})

        qf = QueryFactory(
            table_name=table_name,
            columns=select_columns,
            where_conditions=where_conditions,
            order_by=f"relation_value",
            order=order,
            limit=limit,
            distinct=False,
        )
        qf.make_select()
        return self.run_query(qf.query)

    def run_query(self, query: str):
        if self.connection:
            with self.connection.cursor(dictionary=True) as cursor:
                print("Executing query:", query)
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        else:
            print("No connection to the database.")
            return None
