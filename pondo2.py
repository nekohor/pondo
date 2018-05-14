import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
# from datetime import datetime

matplotlib.style.use('ggplot')
plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
plt.rcParams["axes.unicode_minus"] = False


class CoilIdTable():

    def __init__(self, setup_dict):
        self.root_dir = setup_dict["root_dir"]
        self.table = pd.read_excel(
            os.path.join(self.root_dir, setup_dict["coil_id_table_filename"]))
        self.data_dir = setup_dict["data_dir"]
        self.coil_id_col = setup_dict["coil_id_col"]
        self.date_col = setup_dict["date_col"]
        self.table.index = self.table[self.coil_id_col]

        if not os.path.exists(setup_dict["result_dir"]):
            if "." in setup_dict["result_dir"]:
                pass
            else:
                os.makedirs(setup_dict["result_dir"])

        if self.date_col:
            self.table[self.date_col] = pd.to_datetime(
                self.table[self.date_col])
        else:
            pass

    def get_dca_path(self, coil_id):
        if self.date_col:
            return self.date_dca_path(coil_id)
        else:
            return self.custom_dca_path(coil_id)

    def to_month(self, ts):
        return ts.year * 100 + ts.month

    def to_date(self, ts):
        return ts.year * 10000 + ts.month * 100 + ts.day

    def date_dca_path(self, coil_id):
        ts = self.table.loc[coil_id, self.date_col]
        product_month = self.to_month(ts)
        product_date = self.to_date(ts)
        return "/".join([self.data_dir,
                         "{}".format(product_month),
                         "{}".format(product_date),
                         coil_id])

    def custom_dca_path(self, coil_id):
        return "/".join([self.data_dir,
                         coil_id])


class TaskTable():
    def __init__(self, line):
        self.table = pd.read_excel("../pondo/task_table.xlsx")
        self.table = self.table.loc[self.table["LINE"] == line]


class SemiTaskTable():
    def __init__(self, line):
        self.table = pd.read_excel("../pondo/semi_task_table.xlsx")
        self.table = self.table.loc[self.table["LINE"] == line]
        self.table.index = self.table["ITEM"]


class PartTable():

    def __init__(self, line):
        self.table = pd.read_excel("../pondo/part_table.xlsx")
        self.table = self.table.loc[self.table["LINE"] == line]

    def build_part_table(self, part):
        self.part_table = self.table.loc[self.table["PART"] == part]
        self.idx = self.part_table.index[0]

    def signal_name(self, part):
        self.build_part_table(part)
        return self.part_table.loc[
            self.idx, "SIGNAL"].replace('\\\\', '\\')

    def dca_file(self, part, dca_path):
        self.build_part_table(part)
        single_dca_file = self.part_table.loc[
            self.idx, "DCAFILE"] + "_POND.dca"
        return "/".join([dca_path, single_dca_file])


class PondReader():

    def __init__(self, dcafile, signalname):
        print(dcafile)
        print(signalname)
        self.raw_cmd = "C:/Windows/pndex.exe"
        self.cmd = " ".join([self.raw_cmd, dcafile, signalname])
        self.p = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE).stdout
        self.raw_seires = pd.Series(self.p.read().decode().split(","))
        print(self.raw_seires)
        if (self.raw_seires.size == 1) & (self.raw_seires[0] == ""):
            self.series = pd.Series([])
        else:
            self.series = pd.to_numeric(self.raw_seires)


class PondIndicator():

    def __init__(self, part_table, dca_path):
        self.pt = part_table
        self.dca_path = dca_path

    def set_aim(self, rule, cid, coil_id):
        if str(rule["AIM"]) == "0":
            pass
        else:
            self.aim = cid.table.loc[coil_id, rule["AIM"]]

    def merge(self, *part_args):
        if len(part_args) == 1:
            return self.single_calc(*part_args)
        elif len(part_args) == 2:
            return self.double_calc(*part_args)
        elif len(part_args) == 3:
            return self.triple_calc(*part_args)
        else:
            raise Exception("wrong part args")

    def single_calc(self, cl_part):
        return PondReader(
            self.pt.dca_file(cl_part, self.dca_path),
            self.pt.signal_name(cl_part)).series

    def double_calc(self, os_part, ds_part):
        os_pr = PondReader(
            self.pt.dca_file(os_part, self.dca_path),
            self.pt.signal_name(os_part))
        ds_pr = PondReader(
            self.pt.dca_file(ds_part, self.dca_path),
            self.pt.signal_name(ds_part))
        return (os_pr.series - ds_pr.series)

    def triple_calc(self, cl_part, os_part, ds_part, inverse=False):
        pr = {}
        part_list = [cl_part, os_part, ds_part]
        for part in part_list:
            pr[part] = PondReader(
                self.pt.dca_file(part, self.dca_path),
                self.pt.signal_name(part))

        the_series = ((pr[os_part].series + pr[ds_part].series) / 2 -
                      pr[cl_part].series)

        if inverse:
            return the_series
        else:
            return -the_series

    def is_inverse(self, inverse):
        if inverse == 1:
            return True
        else:
            return False

    def part_convergence(self, rule):
        p_count = rule["P_COUNT"]
        if p_count == 1:
            self.conv_series = self.single_calc(
                rule["PART_CL"])
        elif p_count == 2:
            self.conv_series = self.double_calc(
                rule["PART_OS"],
                rule["PART_DS"])
        elif p_count == 3:
            self.conv_series = self.triple_calc(
                rule["PART_CL"],
                rule["PART_OS"],
                rule["PART_DS"],
                self.is_inverse(rule["INVERSE"]))

    def data_processing(self, rule):
        self.data_series = self.conv_series.loc[self.conv_series.notnull()]
        self.segment_handle(rule)
        return self.algorithm_run(rule)

    def segment_handle(self, rule):
        segment = rule["SEGMENT"]
        total_len = self.data_series.shape[0]
        hd_index = rule["HD_LEN"]
        tl_index = total_len - rule["TL_LEN"]
        if segment == "head":
            self.data_series = self.data_series[:hd_index]
        elif segment == "main":
            self.data_series = self.data_series[hd_index:tl_index]
        elif segment == "tail":
            self.data_series = self.data_series[tl_index:]
        elif segment == "total":
            pass
        else:
            raise Exception("wrong segment")

    def algorithm_run(self, rule):
        algorithm = rule["CALC"]
        if algorithm == "max":
            return self.data_series.max()
        elif algorithm == "min":
            return self.data_series.min()
        elif algorithm == "mean":
            return self.data_series.mean()
        elif algorithm == "std":
            return self.data_series.std()
        elif algorithm == "first":
            return self.data_series[0]
        elif algorithm == "aimrate":
            return self.aimrate(rule)
        else:
            raise Exception("wrong algorithm")

    def aimrate(self, rule):
        tol = rule["TOL"]
        up_lvl = rule["UPPER"]
        lo_lvl = rule["LOWER"]
        ss = self.data_series
        if tol == 0:
            try:
                rate = round(ss.loc[(ss <= up_lvl) & (ss >= lo_lvl)].shape[0] /
                             ss.shape[0] * 100, 2)
            except ZeroDivisionError:
                rate = np.nan
        elif rule["AIM"] == 0:
            try:
                rate = round(ss.loc[ss.abs() <= tol].shape[0] /
                             ss.shape[0] * 100, 2)
            except ZeroDivisionError:
                rate = np.nan
        else:
            rate = round(ss.loc[(ss - self.aim).abs() <= tol].shape[0] /
                         ss.shape[0] * 100, 2)
        return rate


class PondTask(object):

    def __init__(self, setup_dict):
        self.setup_dict = setup_dict
        self.part_table = PartTable(setup_dict["line"])
        self.cid = CoilIdTable(setup_dict)

    def get_total_data(self, *part_args, result_dir):
        self.MAX_INDEX = 1500
        self.raw_df = pd.DataFrame(index=range(0, self.MAX_INDEX))
        for coil_id in self.cid.table.index:
            pi = PondIndicator(
                self.part_table,
                self.cid.get_dca_path(coil_id))
            self.raw_df[coil_id] = pi.merge(*part_args)
            print("Complete {}! data got".format(coil_id))
        self.raw_df.to_excel(result_dir)

    def get_task_stat(self, result_dir):
        self.tsk_tbl = TaskTable(self.setup_dict["line"])
        df = pd.DataFrame()
        for coil_id in self.cid.table.index:
            pi = PondIndicator(
                self.part_table,
                self.cid.get_dca_path(coil_id))
            for task in self.tsk_tbl.table.index:
                rule = self.tsk_tbl.table.loc[task]
                pi.set_aim(rule, self.cid, coil_id)
                pi.part_convergence(rule)
                df.loc[coil_id, self.concat_column(rule)] = (
                    pi.data_processing(rule))
            print("Complete {}!".format(coil_id))
        df.to_excel(result_dir)

    def concat_column(self, rule):
        return ("_".join([rule["ITEM"], rule["CALC"]])).upper()


def name_fmt(setup_dict):
    return "_{}.xlsx".format(setup_dict["line"])


def pondo(setup_dict):
    tsk_obj = PondTask(setup_dict)
    tsk_obj.get_task_stat(setup_dict["result_dir"])


def pondo_total(setup_dict, *args):
    tsk_obj = PondTask(setup_dict)
    tsk_obj.get_total_data(*args, setup_dict["result_dir"])


def pondo_total_batch(setup_dict):
    tsk_obj = PondTask(setup_dict)
    semi_tsk_tbl = SemiTaskTable(setup_dict["line"])
    data_dest = setup_dict["result_dir"] + "/{}" + name_fmt(setup_dict)
    for semi_task in semi_tsk_tbl.table.index:
        rule = semi_tsk_tbl.table.loc[semi_task]
        p_count = rule["P_COUNT"]
        if p_count == 1:
            tsk_obj.get_total_data(
                rule["PART_CL"],
                result_dir=data_dest.format(semi_task))
        elif p_count == 2:
            tsk_obj.get_total_data(
                rule["PART_OS"],
                rule["PART_DS"],
                result_dir=data_dest.format(semi_task))
        elif p_count == 3:
            tsk_obj.get_total_data(
                rule["PART_CL"],
                rule["PART_OS"],
                rule["PART_DS"],
                result_dir=data_dest.format(semi_task))
