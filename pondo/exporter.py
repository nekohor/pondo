from rollen.utils import TimeUtils
from rollen.utils import CoilUtils

from rollen.service import CidService
from rollen.service import DirectoryService
from rollen.service import ResultService

from pondo.assembler import ParamAssembler

from pondo.client import HttpClient
from pondo.client import TcpClient

from pondo.saver import Saver

import pandas as pd


class Exporter():

    def __init__(self, factor_names,
                 record_type="mes", protocol_type="tcp",
                 max_idx_num=1200):

        self.factor_names = factor_names
        self.record_type = record_type
        self.protocol_type = protocol_type
        self.max_idx_num = max_idx_num

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

    def get_df(self, factor_name):

        df = pd.DataFrame(index=range(self.max_idx_num))
        for idx in self.records.index:

            record = self.records.loc[idx]
            coil_id = record["coil_id"]

            df[coil_id] = pd.Series(
                self.get_result(factor_name, record)[
                    "factors"][factor_name]["data"]
            )

            print(record["coil_id"],
                  factor_name,
                  record["start_date"],
                  df.loc[df[coil_id].notnull()].shape[0])

        return df

    def get_params(self, rule, record):

        assembler = ParamAssembler("export")
        assembler.set_rule(rule)
        assembler.set_record(record)
        params = assembler.get_params()

        return params

    def get_result(self, rule, record):

        if self.protocol_type == "http":
            return self.get_result_by_http(rule, record)
        elif self.protocol_type == "tcp":
            return self.get_result_by_tcp(rule, record)
        else:
            raise Exception("unmatched protocol_type")

    def get_result_by_http(self, rule, record):
        cli = HttpClient()
        cli.send_request("exports", self.get_params(rule, record))
        result = cli.get_response()
        return result

    def get_result_by_tcp(self, rule, record):
        cli = TcpClient()
        cli.send_request(self.get_params(rule, record))
        response = cli.get_response()
        return response

    def get_result_by_oci(self, rule, record):
        pass

    def batch_export(self, line, start_date, end_date):

        self.records = self.get_records_by_dates(line, start_date, end_date)
        for factor_name in self.factor_names:

            df = self.get_df(factor_name)
            filepath = (
                Saver(factor_name).get_batch_export_filepath(
                    line, start_date, end_date)
            )
            df.to_excel(filepath)

    def normal_export(self, export_type, coil_ids):

        self.records = self.get_records_by_coil_ids(coil_ids)
        for factor_name in self.factor_names:
            df = self.get_df(factor_name)
            filepath = Saver(factor_name).get_export_filepath(export_type)
            df.to_excel(filepath)

    def current_export(self, cur_dir):
        coil_ids = CoilUtils.get_coil_ids_in_dir(cur_dir)
        self.normal_export("current", coil_ids)

    def specific_export(self, coil_ids):
        self.normal_export("specific", coil_ids)
