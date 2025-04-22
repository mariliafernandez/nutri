import mysql.connector
from typing import Literal


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
        description_like: str = "",
        id: int = None,
        order_by: str = "",
        order: Literal["ASC", "DESC"] = "ASC",
    ):
        conditions = []
        if description_like != "":
            conditions.append({"description": description_like})
        if id is not None:
            conditions.append({"id": id})

        query_factory = QueryFactory(
            table_name=table_name,
            columns=columns,
            where_conditions=conditions,
            order_by=order_by,
            order=order,
        )
        query_factory.make_select()

        with self.connection.cursor(dictionary=True) as cursor:
            print("Executing query:", query_factory.query)
            cursor.execute(query_factory.query)
            result = cursor.fetchall()
            return result


class QueryFactory:
    def __init__(
        self,
        table_name,
        columns: str = "*",
        where_conditions: list = [dict],
        order_by: str = "",
        order: Literal["ASC", "DESC"] = "ASC",
    ):

        self.table_name = table_name
        self.columns = columns
        self.order_by = order_by
        self.order = order
        self.where_conditions = where_conditions
        self.query = ""

    def make_select(self):
        self.select()
        self.add_where_clause()
        self.add_order_by()

    def select(self):
        self.query = f"SELECT {self.columns} FROM {self.table_name}"
        return self.query

    def add_where_clause(self):
        where_clauses = []
        for condition in self.where_conditions:
            column, value = list(condition.items())[0]
            if isinstance(value, str):
                where_clauses.append(f"{column} LIKE '%{value}%'")
            else:
                where_clauses.append(f"{column} = {value}")
        self.query += " WHERE " + " AND ".join(where_clauses)

    def add_order_by(self):
        if self.order_by != "":
            self.query += f" ORDER BY {self.order_by} {self.order}"

    def insert(self, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})", tuple(
            data.values()
        )
