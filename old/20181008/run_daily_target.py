from pondo3 import pondo_all
import os
import sys
import numpy as np
import pandas as pd


line = int(sys.argv[1])
root_dir = sys.argv[2].replace("\\", "/")
data_dir = os.path.join(root_dir, "data")
coil_id_col = "coil_id"

coil_id_table_name = "coil_id_table.xlsx"
task_table_name = sys.path[0] + "/tasks/task_table_thk_all.xlsx"

setup_dict = {}
setup_dict["line"] = line
setup_dict["root_dir"] = root_dir
setup_dict["coil_id_table_name"] = coil_id_table_name
setup_dict["task_table_name"] = task_table_name
setup_dict["data_dir"] = data_dir

# build coil_id_table
coil_id_list = os.listdir(data_dir)
df = pd.DataFrame()
df[coil_id_col] = coil_id_list
df.to_excel(os.path.join(root_dir, coil_id_table_name))

# columns dump in English
setup_dict["coil_id_col"] = coil_id_col
setup_dict["date_col"] = ""

result_dir = os.path.join(root_dir, "curve_matrix")
setup_dict["result_dir"] = result_dir


print(setup_dict)
pondo_all(setup_dict)

summary = pd.DataFrame()
df = pd.read_excel(result_dir + "/thick_clg.xlsx")

head_cut = 5
tail_cut = 5
head_len = 50
tail_len = 50
lim_list = [0.05, 0.03]
for coil_id in df.columns:
    val = 0
    curve_srs = df.loc[df[coil_id].notnull()][coil_id]
    for lim in lim_list:
        if curve_srs.shape[0] == 0:
            val = np.nan
            summary.loc[coil_id, "HEAD_THK_AIMRATE_{}".format(lim)] = val
            summary.loc[coil_id, "TOTAL_THK_AIMRATE_{}".format(lim)] = val
        else:
            head_srs = curve_srs[head_cut:head_len]
            print(head_srs)
            print(head_srs[(head_srs > -lim) & (head_srs < lim)])
            print(head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0])
            print(head_srs.shape[0])
            summary.loc[coil_id, "HEAD_THK_AIMRATEE_{}".format(lim)] = round(
                head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0] /
                head_srs.shape[0] * 100, 2)
            summary.loc[coil_id, "TOTAL_THK_AIMRATE_{}".format(lim)] = round(
                curve_srs[(curve_srs > -lim) & (curve_srs < lim)].shape[0] /
                curve_srs.shape[0] * 100, 2)

df = pd.read_excel(result_dir + "/sym_flt_del.xlsx")
head_cut = 5
tail_cut = 5
if line == 1580:
    head_len = 120
elif line == 2250:
    head_len = 150
else:
    raise Exception("wrong line")
tail_len = 50
lim_list = [50, 30, 20, 10, 5]
for coil_id in df.columns:
    val = 0
    curve_srs = df.loc[df[coil_id].notnull()][coil_id]
    for lim in lim_list:
        if curve_srs.shape[0] == 0:
            val = np.nan
            summary.loc[coil_id, "HEAD_SYM_FLT_AIMRATE_{}".format(lim)] = val
            summary.loc[coil_id, "TOTAL_SYM_FLT_AIMRATE_{}".format(lim)] = val
        else:
            head_srs = curve_srs[head_cut:head_len]
            print(head_srs)
            print(head_srs[(head_srs > -lim) & (head_srs < lim)])
            print(head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0])
            print(head_srs.shape[0])
            summary.loc[coil_id, "HEAD_SYM_FLT_AIMRATEE_{}".format(lim)] = round(
                head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0] /
                head_srs.shape[0] * 100, 2)
            summary.loc[coil_id, "TOTAL_SYM_FLT_AIMRATE_{}".format(lim)] = round(
                curve_srs[(curve_srs > -lim) & (curve_srs < lim)].shape[0] /
                curve_srs.shape[0] * 100, 2)

df = pd.read_excel(result_dir + "/asym_flt_del.xlsx")
head_cut = 5
tail_cut = 5
if line == 1580:
    head_len = 120
elif line == 2250:
    head_len = 150
else:
    raise Exception("wrong line")
tail_len = 50
lim_list = [20]
for coil_id in df.columns:
    val = 0
    curve_srs = df.loc[df[coil_id].notnull()][coil_id]
    for lim in lim_list:
        if curve_srs.shape[0] == 0:
            val = np.nan
            summary.loc[coil_id, "HEAD_ASYM_FLT_AIMRATE_{}".format(lim)] = val
            summary.loc[coil_id, "TOTAL_ASYM_FLT_AIMRATE_{}".format(lim)] = val
        else:
            head_srs = curve_srs[head_cut:head_len]
            print(head_srs)
            print(head_srs[(head_srs > -lim) & (head_srs < lim)])
            print(head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0])
            print(head_srs.shape[0])
            summary.loc[coil_id, "HEAD_ASYM_FLT_AIMRATEE_{}".format(lim)] = round(
                head_srs[(head_srs > -lim) & (head_srs < lim)].shape[0] /
                head_srs.shape[0] * 100, 2)
            summary.loc[coil_id, "TOTAL_ASYM_FLT_AIMRATE_{}".format(lim)] = round(
                curve_srs[(curve_srs > -lim) & (curve_srs < lim)].shape[0] /
                curve_srs.shape[0] * 100, 2)

summary.to_excel(root_dir + "/data_result.xlsx")
