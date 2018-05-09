import subprocess
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
matplotlib.style.use('ggplot')
plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
plt.rcParams["axes.unicode_minus"] = False


class PartTable():

    def __init__(self, line, part):
        self.table = pd.read_excel("../pondo/part_table.xlsx")
        self.part_table = self.table.loc[
            (self.table["LINE"] == line) & (self.table["PART"] == part)]
        print(part)
        self.index = self.part_table.index[0]
        self.signal_name = self.part_table.loc[
            self.index, "SIGNAL"].replace('\\\\', '\\')
        self.single_dca_file = self.part_table.loc[
            self.index, "DCAFILE"] + "_POND.dca"

    def get_month(self, the_date):
        return the_date // 100

    def get_dca_file(self, data_dir, product_date, coil_id):
        if product_date:
            return self.date_dca_file(data_dir, product_date, coil_id)
        else:
            return self.custom_dca_file(data_dir, coil_id)

    def date_dca_file(self, data_dir, product_date, coil_id):
        return "/".join([data_dir,
                         "{}".format(self.get_month(product_date)),
                         "{}".format(product_date),
                         coil_id,
                         self.single_dca_file])

    def luna_dca_file(self, data_dir, month, product_date, coil_id):
        return "/".join([data_dir,
                         "{}".format(month),
                         "{}".format(product_date),
                         coil_id,
                         self.single_dca_file])

    def custom_dca_file(self, data_dir, coil_id):
        print(data_dir, coil_id, self.single_dca_file)
        return "/".join([data_dir,
                         coil_id,
                         self.single_dca_file])


class PondReader():

    def __init__(self, dcafile, signalname):
        print(dcafile)
        print(signalname)
        self.raw_cmd = "pndex.exe"
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

    def __init__(self, line, data_dir, product_date, coil_id):
        self.line = line
        self.data_dir = data_dir
        self.product_date = product_date
        self.coil_id = coil_id

    def inject_aim(self, root_series, task_series):
        aim_col = task_series["AIM"]
        if aim_col == 0:
            pass
        else:
            self.aim = root_series[aim_col]

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
        pt = PartTable(self.line, cl_part)
        pr = PondReader(pt.get_dca_file(
            self.data_dir, self.product_date, self.coil_id),
            pt.signal_name)
        return pr.series

    def double_calc(self, os_part, ds_part):
        pt = {}
        pt["os"] = PartTable(self.line, os_part)
        pt["ds"] = PartTable(self.line, ds_part)

        pr = {}
        for k, v in pt.items():
            pr[k] = PondReader(v.get_dca_file(
                self.data_dir, self.product_date, self.coil_id),
                v.signal_name)

        return (pr["os"].series - pr["ds"].series)

    def triple_calc(self, cl_part, os_part, ds_part, inverse=False):
        pt = {}
        pt["cl"] = PartTable(self.line, cl_part)
        pt["os"] = PartTable(self.line, os_part)
        pt["ds"] = PartTable(self.line, ds_part)

        pr = {}
        for k, v in pt.items():
            pr[k] = PondReader(v.get_dca_file(
                self.data_dir, self.product_date, self.coil_id),
                v.signal_name)

        the_series = ((pr["os"].series + pr["ds"].series) / 2 -
                      pr["cl"].series)

        if inverse:
            return -the_series
        else:
            return the_series

    def choose_inverse(self, inverse):
        if inverse == 1:
            return True
        else:
            return False

    def part_convergence(self, task_series):
        p_count = task_series["P_COUNT"]
        if p_count == 1:
            self.part_series = self.single_calc(
                task_series["PART_CL"])
        elif p_count == 2:
            self.part_series = self.double_calc(
                task_series["PART_OS"],
                task_series["PART_DS"])
        elif p_count == 3:
            self.part_series = self.triple_calc(
                task_series["PART_CL"],
                task_series["PART_OS"],
                task_series["PART_DS"],
                self.choose_inverse(task_series["INVERSE"]))

    def data_processing(self, task_series):
        self.data_series = self.part_series.loc[self.part_series.notnull()]
        self.segment_handle(task_series)
        return self.algorithm_handle(task_series)

    def segment_handle(self, task_series):
        segment = task_series["SEGMENT"]
        total_len = self.data_series.shape[0]
        hd_index = task_series["HD_LEN"]
        tl_index = total_len - task_series["TL_LEN"]
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

    def algorithm_handle(self, task_series):
        algorithm = task_series["CALC"]
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
            return self.aimrate(task_series)
        else:
            raise Exception("wrong algorithm")

    def aimrate(self, task_series):
        tol = task_series["TOL"]
        ss = self.data_series
        if task_series["AIM"] == 0:
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

    def __init__(self, line, coil_id_table, data_dir):
        self.line = line
        self.coil_id_table = coil_id_table
        self.data_dir = data_dir

    def dump_setup(self, coil_id_col, product_date_col=None, aim_col=None):
        self.coil_id_col = coil_id_col
        self.product_date_col = product_date_col
        self.aim_col = aim_col
        self.coil_id_table.index = self.coil_id_table[coil_id_col]
        if self.product_date_col:
            self.coil_id_table[self.product_date_col] = pd.to_datetime(
                self.coil_id_table[self.product_date_col])
        else:
            pass

    def generate_date(self, coil_id):
        if self.product_date_col:
            ts = self.coil_id_table.loc[coil_id, self.product_date_col]
            return ts.year * 10000 + ts.month * 100 + ts.day
        else:
            return None

    def get_total_data(self, *part_args, result_dir):
        self.MAX_INDEX = 1500
        self.raw_df = pd.DataFrame(index=range(0, self.MAX_INDEX))
        for coil_id in self.coil_id_table.index:
            pi = PondIndicator(self.line, self.data_dir,
                               self.generate_date(coil_id), coil_id)
            self.raw_df[coil_id] = pi.merge(*part_args)
            print("Complete {}! data got".format(coil_id))
        self.raw_df.to_excel(result_dir)

    def task_operation(self, result_dir):
        # ===task table===
        self.task_table = pd.read_excel("../pondo/task_table.xlsx")
        self.task_table = self.task_table.loc[
            self.task_table["LINE"] == self.line]
        self.df = pd.DataFrame()
        for coil_id in self.coil_id_table.index:
            pi = PondIndicator(self.line, self.data_dir,
                               self.generate_date(coil_id), coil_id)
            for task in self.task_table.index:
                task_series = self.task_table.loc[task]
                pi.inject_aim(self.coil_id_table.loc[coil_id],
                              task_series)
                pi.part_convergence(task_series)
                self.df.loc[coil_id, self.conv_col(task_series)
                            ] = pi.data_processing(task_series)
            print("Complete {}!".format(coil_id))
        self.df.to_excel(result_dir)

    def conv_col(self, task_series):
        return ("_".join([task_series["ITEM"], task_series["CALC"]])).upper()


def pondo(**kwargs):
    # ============== 10 setups ======================
    for k in kwargs:
        line = kwargs["line"]
        coil_id_table_filename = kwargs["coil_id_table_filename"]
        data_dir = kwargs["data_dir"]
        coil_id_col = kwargs["coil_id_col"]
        product_date_col = kwargs["product_date_col"]
        result_dir = kwargs["result_dir"]

    coil_id_table = pd.read_excel(coil_id_table_filename)
    # ==============================================
    tsk_obj = PondTask(line, coil_id_table, data_dir)
    tsk_obj.dump_setup(coil_id_col, product_date_col)
    tsk_obj.task_operation(result_dir)
# tsk_obj.get_total_data("test.xlsx")


def pondo_total(**kwargs):
    # ============== 10 setups ======================
    for k in kwargs:
        line = kwargs["line"]
        coil_id_table_filename = kwargs["coil_id_table_filename"]
        data_dir = kwargs["data_dir"]
        coil_id_col = kwargs["coil_id_col"]
        product_date_col = kwargs["product_date_col"]
        result_dir = kwargs["result_dir"]

    coil_id_table = pd.read_excel(coil_id_table_filename)
    # ==============================================
    tsk_obj = PondTask(line, coil_id_table, data_dir)
    tsk_obj.dump_setup(coil_id_col, product_date_col)
    tsk_obj.get_total_data("thick_clg", result_dir)
