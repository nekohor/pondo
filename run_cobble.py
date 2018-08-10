from pondo3 import pondo_all
import os
import sys
import pandas as pd

print(sys.path[0])
print(os.getcwd())  # 获得当前工作目录
print(os.path.abspath('.'))  # 获得当前工作目录
print(os.path.abspath('..'))  # 获得当前工作目录的父目录
print(os.path.abspath(os.curdir))  # 获得当前工作目录


line = int(sys.argv[1])
root_dir = sys.argv[2].replace("\\", "/")
data_dir = os.path.join(root_dir, "data")
coil_id_col = "coil_id"

coil_id_table_name = "coil_id_table.xlsx"
task_table_name = sys.path[0] + "/tasks/task_table_cobble.xlsx"

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
