import os
import sys
import subprocess
# import matplotlib.pyplot as plt
# import matplotlib
import pandas as pd
import numpy as np

# matplotlib.style.use('ggplot')
# plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
# plt.rcParams["axes.unicode_minus"] = False


class CoilIdTable():

    def __init__(self, setup_dict):
        self.root_dir = setup_dict["root_dir"]
        self.table = pd.read_excel(
            os.path.join(self.root_dir, setup_dict["coil_id_table_name"]))
        self.data_dir = setup_dict["data_dir"]
        self.coil_id_col = setup_dict["coil_id_col"]
        self.date_col = setup_dict["date_col"]
        self.result_dir = setup_dict["result_dir"]
        self.table.index = self.table[self.coil_id_col]

        if not os.path.exists(self.result_dir):
            if "." in self.result_dir:
                pass
            else:
                os.makedirs(self.result_dir)

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
        print(ts)
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

    def __init__(self, task_table_name):
        self.table = pd.read_excel(task_table_name)


class PartTable():

    def __init__(self, line):
        self.table = pd.read_excel(sys.path[0] + "/part_table.xlsx")
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
        single_dca_file = self.part_table.loc[self.idx, "DCAFILE"] + ".dca"
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


class HDTLLengthProcess():

    def __init__(self, rule, cid_record, setup_dict):
        self.line = setup_dict["line"]
        self.rule = rule
        self.cid_record = cid_record
        self.setup_dict = setup_dict
        self.main_process()

    def main_process(self):
        # normal head and tail len
        if 1580 == self.line:
            self.head_len = 120
            self.tail_len = 70
        elif 2250 == self.line:
            self.head_len = 150
            self.tail_len = 70
        else:
            raise Exception("wrong line")

        # coil length is not match the sum of hdtal len
        coil_length = self.cid_record[self.setup_dict["coil_len_col"]]
        if (self.head_len + self.tail_len) > coil_length:
            self.head_len = int(coil_length * 0.33)
            self.tail_len = int(coil_length * 0.33)

        # about thick
        if self.rule["ITEM"] == "thick_clg":
            aim_thick = self.cid_record[self.setup_dict["aim_thick_col"]]
            if np.isnan(aim_thick):
                self.head_len = 10
            else:
                self.head_len = round(np.interp(
                    aim_thick,
                    np.linspace(0, 25),
                    np.linspace(7, 15)))
            self.tail_len = 50

    def dual_length(self):
        return (self.head_len, self.tail_len)


class BoundaryProcess():

    def __init__(self, rule, cid_record, setup_dict):
        self.rule = rule
        self.cid_record = cid_record
        self.setup_dict = setup_dict
        self.aim_thick_col = setup_dict["aim_thick_col"]
        self.build_bound()

    def build_tolerance_by_thick(self):
        if np.isnan(self.rule["TOL_PERC"]):
            self.lower = -self.rule["TOL"]
            self.upper = self.rule["TOL"]
        else:
            tol = (self.rule["TOL_PERC"] / 100 *
                   self.cid_record[self.aim_thick_col])
            self.lower = -np.maximum(tol, self.rule["TOL_MAX"])
            self.upper = np.maximum(tol, self.rule["TOL_MAX"])

    def build_tolerance_by_aim(self):
        aim = self.build_aim(self.rule["AIM"])
        self.lower = aim - self.rule["TOL"]
        self.upper = aim + self.rule["TOL"]

    def build_aim(self, aim_tag):
        return self.cid_record[self.setup_dict["aim_{}_col".format(aim_tag)]]

    def build_tolerance(self):
        print(str(self.rule["AIM"]))
        if str(self.rule["AIM"]) == "nan":
            self.lower = 0
            self.upper = 0
        elif (str(self.rule["AIM"]) == "0") or (
                str(self.rule["AIM"]) == "0.0"):
            self.build_tolerance_by_thick()
        else:
            self.build_tolerance_by_aim()

    def build_bound(self):
        if np.isnan(self.rule["UPPER"]) & np.isnan(self.rule["LOWER"]):
            self.build_tolerance()
        else:
            self.upper = self.rule["UPPER"]
            self.lower = self.rule["LOWER"]

    def dual_bound(self):
        return (self.upper, self.lower)


class PondItem():

    def __init__(self, part_tbl, dca_path):
        self.part_tbl = part_tbl
        self.dca_path = dca_path

    def pre_handle(self, rule):
        p_count = rule["PC"]
        self.dca_file = ""
        self.signals = []
        if p_count == 1:
            self.dca_file = self.part_tbl.dca_file(
                rule["PART_CL"], self.dca_path)
            self.signals = [self.part_tbl.signal_name(rule["PART_CL"])]
        elif p_count == 2:
            self.dca_file = self.part_tbl.dca_file(
                rule["PART_OS"], self.dca_path)
            self.signals = [self.part_tbl.signal_name(rule["PART_OS"]),
                            self.part_tbl.signal_name(rule["PART_DS"])]
        elif p_count == 3:
            self.dca_file = self.part_tbl.dca_file(
                rule["PART_CL"], self.dca_path)
            self.signals = [self.part_tbl.signal_name(rule["PART_CL"]),
                            self.part_tbl.signal_name(rule["PART_OS"]),
                            self.part_tbl.signal_name(rule["PART_DS"])]
        else:
            raise Exception("wrong p count")

        self.stat_name = rule["STAT_FN"]
        self.seg_name = rule["SEGMENT"]

    def hdtl_len_handle(self, len_process):
        self.head_len, self.tail_len = len_process.dual_length()

    def hdtl_cut_handle(self, rule):
        if "r2dt" == rule["PART_CL"].lower():
            self.head_cut = 5
            self.tail_cut = 15
        else:
            self.head_cut = 5
            self.tail_cut = 4

    def boundary_handle(self, bound_process):
        self.upper, self.lower = bound_process.dual_bound()

    def calc_run(self):
        self.raw_cmd = "C:/Windows/pondex.exe"
        self.argv = []
        self.argv.append(self.raw_cmd)
        self.argv.append(self.dca_file)
        self.argv.extend(self.signals)
        self.argv.extend([self.stat_name, self.seg_name])
        self.argv.extend(
            [str(self.head_len), str(self.tail_len),
             str(self.head_cut), str(self.tail_cut)])
        self.argv.extend([str(self.upper), str(self.lower)])
        self.cmd = " ".join(self.argv)
        # print(self.cmd)
        self.p = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE).stdout
        self.calc_result_str = self.p.read().decode()

    def post_handle(self, rule):
        try:
            self.calc_result = float(self.calc_result_str)
        except Exception as e:
            self.nan_and_array_handle()
        else:
            if ((rule["STAT_FN"] in ["max", "min"]) & (
                    rule["PART_CL"] == "flt_ro3")):
                self.calc_result = -self.calc_result
            else:
                pass
        finally:
            pass

    def nan_and_array_handle(self):
        if self.calc_result_str == "":
            self.calc_result = np.nan
        else:
            pass

    def all_run(self):
        self.raw_cmd = "C:/Windows/pondex.exe"
        self.argv = []
        self.argv.append(self.raw_cmd)
        self.argv.append(self.dca_file)
        self.argv.extend(self.signals)
        self.argv.extend([self.stat_name, self.seg_name])
        self.argv.extend(
            [str(0), str(0),
             str(0), str(0)])
        self.argv.extend([str(0), str(0)])
        self.cmd = " ".join(self.argv)
        # print(self.cmd)
        self.p = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE).stdout
        self.raw_seires = pd.Series(self.p.read().decode().split(","))
        print(self.raw_seires)
        if (self.raw_seires.size == 1) & (self.raw_seires[0] == ""):
            self.series = pd.Series([])
        else:
            self.series = pd.to_numeric(self.raw_seires)
        # all_run
        self.calc_result = self.series

    def result(self):
        return self.calc_result


class PondTask(object):

    def __init__(self, setup_dict):
        self.setup_dict = setup_dict
        self.cid = CoilIdTable(setup_dict)
        self.part_tbl = PartTable(setup_dict["line"])
        self.tsk_tbl = TaskTable(setup_dict["task_table_name"])

    def task_exec(self):
        df = pd.DataFrame()
        for coil_id in self.cid.table.index:
            pi = PondItem(self.part_tbl,
                          self.cid.get_dca_path(coil_id))
            cid_record = self.cid.table.loc[coil_id]
            for task in self.tsk_tbl.table.index:
                rule = self.tsk_tbl.table.loc[task]
                pi.pre_handle(rule)
                pi.hdtl_len_handle(HDTLLengthProcess(
                    rule, cid_record, self.setup_dict))
                pi.hdtl_cut_handle(rule)
                pi.boundary_handle(BoundaryProcess(
                    rule, cid_record, self.setup_dict))
                pi.calc_run()
                pi.post_handle(rule)

                # output
                col_prc = ColumnProcess(rule)
                df.loc[coil_id,
                       col_prc.column()] = pi.result()
                print(col_prc.column())
                print(pi.result())
            print("Complete {}!".format(coil_id))
        df.to_excel(self.cid.result_dir)

    def task_all(self):
        MAX_INDEX = 1500
        df = pd.DataFrame(index=range(0, MAX_INDEX))
        for task in self.tsk_tbl.table.index:
            rule = self.tsk_tbl.table.loc[task]
            for coil_id in self.cid.table.index:
                pi = PondItem(self.part_tbl,
                              self.cid.get_dca_path(coil_id))
                pi.pre_handle(rule)
                pi.all_run()
                df[coil_id] = pi.result()
                print("Complete {}! data got".format(coil_id))
            file_name = rule["ITEM"] + ".xlsx"
            df.to_excel(os.path.join(self.cid.result_dir, file_name))


class ColumnProcess():

    def __init__(self, rule):
        self.rule = rule
        self.col = ""
        self.tolerance_add(self.rule)
        self.flatness_transfer(self.rule)

    def tolerance_attach_old(self, rule):
        if np.isnan(rule["THK_BOT"]) & np.isnan(rule["THK_TOP"]):
            self.lower_to_upper_or_tol(rule)
        else:
            self.col = "_".join([
                rule["SEGMENT"],
                rule["ITEM"],
                rule["STAT_FN"],
                "{:>05.2f}_{:>05.2f}".format(
                    rule["THK_BOT"], rule["THK_TOP"])])

    def build_simple_col(self, rule):
        self.col = "_".join([
            rule["SEGMENT"],
            rule["ITEM"],
            rule["STAT_FN"]])

    def tolerance_add(self, rule):
        if rule["STAT_FN"].lower() == "aimrate":
            self.lower_to_upper_or_tol(rule)
        else:
            self.build_simple_col(rule)

    def lower_to_upper_or_tol(self, rule):
        if np.isnan(rule["LOWER"]) & np.isnan(rule["UPPER"]):
            self.absolute_tol_or_perc_tol(rule)
        else:
            lower_tag = "{}".format(rule["LOWER"])
            upper_tag = "{}".format(rule["UPPER"])
            self.col = "_".join([
                rule["SEGMENT"],
                rule["ITEM"],
                rule["STAT_FN"],
                self.cut_to_int(lower_tag),
                self.cut_to_int(upper_tag)])

    def absolute_tol_or_perc_tol(self, rule):
        if np.isnan(rule["TOL_PERC"]) & np.isnan(rule["TOL_MAX"]):
            self.build_absolute_tol_col(rule)
        else:
            self.build_perc_tol_col(rule)

    def build_absolute_tol_col(self, rule):
        tol_tag = "{}".format(rule["TOL"] * self.mm_to_um(rule))
        self.col = "_".join([
            rule["SEGMENT"],
            rule["ITEM"],
            rule["STAT_FN"],
            self.cut_to_int(tol_tag)])

    def build_perc_tol_col(self, rule):
        tol_max = "{}".format(rule["TOL_MAX"] * self.mm_to_um(rule))
        self.col = "_".join([
            rule["SEGMENT"],
            rule["ITEM"],
            rule["STAT_FN"],
            "{}%".format(rule["TOL_PERC"]),
            "max{}".format(self.cut_to_int(tol_max))])

    def mm_to_um(self, rule):
        if rule["MM_TO_UM"] == 1:
            return 1000
        else:
            return 1

    def cut_to_int(self, tag):
        if tag[-2:] == ".0":
            return tag[:-2]
        else:
            return tag

    def flatness_transfer(self, rule):
        if rule["PART_CL"] == "flt_ro3":
            if rule["STAT_FN"] == "max":
                stat_tag = "min"
            elif rule["STAT_FN"] == "min":
                stat_tag = "max"
            elif rule["STAT_FN"] == "mean":
                stat_tag = "mean"
            elif rule["STAT_FN"] == "all":
                stat_tag = "all"
            elif rule["STAT_FN"] == "std":
                stat_tag = "std"
            else:
                stat_tag = rule["STAT_FN"]
                self.col = "_".join([
                    rule["SEGMENT"],
                    rule["ITEM"],
                    stat_tag,
                    self.cut_to_int("{}".format(rule["TOL"]))
                ])
                return
            self.col = "_".join([
                rule["SEGMENT"],
                rule["ITEM"],
                stat_tag])
        else:
            pass

    def column(self):
        return self.col.upper()


def pondo(setup_dict):
    tsk_obj = PondTask(setup_dict)
    tsk_obj.task_exec()


def pondo_all(setup_dict):
    tsk_obj = PondTask(setup_dict)
    tsk_obj.task_all()
