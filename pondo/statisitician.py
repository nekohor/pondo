from rollen.utils import TimeUtils
from rollen.utils import CoilUtils

from rollen.service import CidService
from rollen.service import DirectoryService
from rollen.service import ResultService

from pondo.task import Task
from pondo.assembler import ParamAssembler

from pondo.client import HttpClient
from pondo.client import TcpClient

from pondo.calculator import Calculator
from pondo.saver import Saver

import pandas as pd
import numpy as np
import redis
import json


class Statistician():

    def __init__(self, task_name, record_type="mes", protocol_type="tcp"):

        self.task_name = task_name
        self.task = Task(self.task_name)

        self.record_type = record_type
        self.protocol_type = protocol_type

        self.saver = Saver(self.task_name)

        self.redis_server = self.get_redis_server()

    def get_redis_server(self):
        redis_server = redis.Redis(host='localhost', port=6379, db=0)
        try:
            redis_server.set('is', 'connected')
        except redis.exceptions.ConnectionError as e:
            print("========================================")
            print(e)
            print("========================================")
            redis_server = None
        return redis_server

    def get_service(self):

        if self.record_type == "ledger":
            return CidService()
        elif self.record_type == "pond":
            return DirectoryService()
        elif self.record_type == "mes":
            return ResultService()
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
        # df = pd.DataFrame(columns=self.task.get_col_names())
        df = pd.DataFrame()
        for idx in self.records.index:

            record = self.records.loc[idx]
            coil_id = record["coil_id"]
            df.loc[idx, "coil_id"] = coil_id

            for rule_id in self.task.get_indexs():

                rule = self.task.get_rule(rule_id)
                col_name = self.task.get_col_name(rule_id)

                df.loc[idx, col_name] = (
                    self.get_result(rule, record)
                )
                print(
                    record["start_date"],
                    coil_id,
                    col_name,
                    df.loc[idx, col_name]
                )
        return df

    def get_result(self, rule, record):

        if self.protocol_type == "http":
            return self.get_result_by_http(rule, record)
        elif self.protocol_type == "tcp":
            return self.get_result_by_tcp(rule, record)
        else:
            raise Exception("unmatched protocol_type")

    def get_assembler(self, assem_type, rule, record):

        assembler = ParamAssembler(assem_type)
        assembler.set_rule(rule)
        assembler.set_record(record)

        return assembler

    def get_result_by_http(self, rule, record):
        cli = HttpClient()
        assembler = self.get_assembler("stat", rule, record)
        cli.send_request("stat", assembler.get_params())

        result = cli.get_response()

        if result == "NaN":
            result = np.nan

        return result

    def get_result_by_tcp(self, rule, record):
        assembler = self.get_assembler("stat", rule, record)
        response = self.get_response_data(rule, record)
        c = Calculator(response, assembler.get_params())
        return c.calculate()

    def get_response_data(self, rule, record):
        if self.redis_server is None:
            data = self.get_response_data_by_default(rule, record)
        else:
            data = self.get_response_data_by_cache(rule, record)
        return data

    def get_response_data_by_cache(self, rule, record):
        assembler = self.get_assembler("stat", rule, record)
        params = assembler.get_params()
        cache_key = params["coilId"] + "_" + params["factorName"]

        if self.redis_server is None:
            data = self.get_response_data_by_default(rule, record)
            self.redis_server.set(cache_key, json.dumps(data))
        else:
            redis_value = self.redis_server.get(cache_key)
            data = json.loads(redis_value.decode().replace("'", '"'))
        # print(data)
        return data

    def get_response_data_by_default(self, rule, record):

        assembler = self.get_assembler("export", rule, record)
        cli = TcpClient()
        cli.send_request(assembler.get_params())

        response = cli.get_response()
        # print(response)
        return response

    def merge_df(self, records, df):
        merged_df = pd.merge(records, df, how="left", on="coil_id")
        del merged_df['cur_dir']
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
