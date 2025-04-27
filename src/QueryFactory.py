from typing import Literal


class QueryFactory:
    def __init__(
        self,
        table_name,
        columns: str = "*",
        where_conditions: list[dict] = [],
        order_by: str = None,
        order: Literal["ASC", "DESC"] = "ASC",
        limit: int = None,
        distinct: bool = False,
    ):

        self.table_name = table_name
        self.columns = columns
        self.order_by = order_by
        self.order = order
        self.where_conditions = where_conditions
        self.limit = limit
        self.query = ""
        self.distinct = distinct

    def make_select(self):
        self.start_select_query(columns=self.columns, table_name=self.table_name)
        conditions = [
            self.condition_ditc2str(condition) for condition in self.where_conditions
        ]
        self.add_where_clause(conditions)
        self.add_order_by(self.order_by, self.order)
        self.add_limit(self.limit)

    def start_select_query(self, columns: str = "*", table_name: str = ""):
        if self.distinct:
            columns = f"DISTINCT {columns}"
        self.query = f"SELECT {columns} FROM {table_name}"
        return self.query

    def add_where_clause(
        self, conditions: list[str], mode: Literal["AND", "OR"] = "AND"
    ):
        if len(conditions) == 1:
            self.query += f" WHERE {conditions[0]}"
        elif len(conditions) > 1:
            aggregator = f" {mode} "
            self.query += f" WHERE {aggregator.join(conditions)}"

    def condition_ditc2str(self, condition: dict):
        column, value = list(condition.items())[0]
        if isinstance(value, str):
            return f"{column} LIKE '%{value}%'"
        elif isinstance(value, list):
            values = ", ".join([f"'{v}'" for v in value])
            return f"{column} IN ({values})"
        else:
            return f"{column} = {value}"

    def add_order_by(self, order_by: str = None, order: Literal["ASC", "DESC"] = "ASC"):
        if order_by is not None:
            self.query += f" ORDER BY {order_by} {order}"

    def add_limit(self, limit: int):
        if limit is not None:
            self.query += f" LIMIT {limit}"

    def make_insert_query(self, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})", tuple(
            data.values()
        )
