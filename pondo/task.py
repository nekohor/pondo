import pandas as pd

from rollen.utils import DirectoryUtils

from pondo.rule import Rule
from pondo.column import ColumnName


class Task():

    def __init__(self, task_name):

        self.task_name = task_name

        self.task_path = (
            DirectoryUtils.get_tasks_dir() +
            "/task_stats_{}.xlsx".format(task_name))

        self.table = pd.read_excel(self.task_path)

        self._columns = self.build_cols()

    def build_cols(self):

        cols = []
        for idx in self.table.index:
            cols.append(ColumnName(Rule(self.table.loc[idx])).get_col())
        return cols

    def get_col_names(self):
        # a list for schemas
        if hasattr(self, "_columns"):
            return self._columns
        else:
            self._columns = self.build_cols()
            return self._columns

    def get_factors(self):
        return self.table["FACTOR"].drop_duplicates()

    def get_indexs(self):
        return self.table.index

    def get_rule(self, idx):
        return Rule(self.table.loc[idx])

    def get_col_name(self, idx):
        return self._columns[idx]

    def get_factor_name(self, idx):
        return self.table.loc[idx, "FACTOR"]

    def is_query_cid(self):

        for aim in self.table["AIM"]:

            if type(aim) == str:
                return True

            if type(aim) == int:
                continue

            if type(aim) == float:
                continue

        return False
