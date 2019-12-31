from rollen.utils import TimeUtils
from rollen.utils import CoilUtils

from rollen.service import CidService
from rollen.service import DirectoryService

from pondo.task import Task
from pondo.assembler import Assembler
from pondo.client import Client
from pondo.saver import Saver

import pandas as pd


class Statistician():

    def __init__(self, task_name, record_type):

        self.task_name = task_name
        self.task = Task(self.task_name)

        self.record_type = record_type

        self.cli = Client()

        self.saver = Saver(self.task_name)

    def get_service(self):

        if self.record_type == "ledger":
            return CidService()
        elif self.record_type == "pond":
            return DirectoryService()
        else:
            raise Exception("unmatched record type in Stats")

    def get_records_by_dates(self, line, start_date, end_date):
        dates = TimeUtils.get_dates(start_date, end_date)
        service = self.get_service()
        records = service.get_data_by_dates(line, dates)
        return records

    def get_records_by_coil_ids(self, coil_ids):
        service = self.get_service()
        records = service.get_data_by_coil_ids(coil_ids)
        return records

    def get_df(self):
        df = pd.DataFrame(columns=self.task.get_col_names())
        for idx in self.records.index:

            record = self.records.loc[idx]
            df.loc[idx, "coil_id"] = record["coil_id"]

            for rule_id in self.task.get_indexs():

                rule = self.task.get_rule(rule_id)
                col_name = self.task.get_col_name(rule_id)

                df.loc[idx, col_name] = (
                    self.get_result("stats", rule, record)
                )
        return df

    def get_result(self, req_type, rule, record):

        assembler = Assembler(req_type)

        assembler.set_rule(rule)
        assembler.set_record(record)

        params = assembler.get_params()
        self.cli.send_request(req_type, params)
        result = self.cli.get_response()

        return result

    def merge_df(self, records, df):
        merged_df = pd.merge(records, df, how="left", on="coil_id")
        return merged_df

    def batch_stat(self, line, start_date, end_date):

        self.records = self.get_records_by_dates(line, start_date, end_date)
        df = self.get_df()
        df = self.merge_df(self.records, df)
        self.saver.save_batch_stat(df, line, start_date, end_date)

    def current_stat(self, cur_dir):

        coil_ids = CoilUtils.get_coil_ids_in_dir(cur_dir)
        self.records = self.get_records_by_coil_ids(coil_ids)
        df = self.get_df()
        df = self.merge_df(self.records, df)
        self.saver.save_stat(df, "current")

    def specific_stat(self, coil_ids):
        self.records = self.get_records_by_coil_ids(coil_ids)
        df = self.get_df()
        df = self.merge_df(self.records, df)
        self.saver.save_stat(df, "specific")
