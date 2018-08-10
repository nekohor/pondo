from pondo3 import pondo
import os


line = 2250

# root_dir = "d:/NutCloudSync/work/20180607_平整浪形质量异议"
# root_dir = "e:/005统计/20180511_M610L浪形预报统计"
# root_dir = "e:/005统计/20180701_刘强统计"
# root_dir = "d:/NutCloudSync/Q235B预报"
# root_dir = "d:/NutCloudSync/M610L预报"
root_dir = "e:/000浪形预测/20180803"

coil_id_table_name = "selected_{}.xlsx".format(line)
origin_result_dir = "data_result_{}.xlsx".format(line)

task_table_name = "tasks/task_table_wav_predict.xlsx"
# task_table_name = "tasks/task_table_small.xlsx"

drive_id = {"1580": "i:/1580hrm", "2250": "h:/2250hrm"}
setup_dict = {}
setup_dict["line"] = line
setup_dict["root_dir"] = root_dir
setup_dict["coil_id_table_name"] = coil_id_table_name
setup_dict["task_table_name"] = task_table_name
setup_dict["data_dir"] = drive_id[str(line)]


# columns dump in Zh_cn
setup_dict["coil_id_col"] = "热卷号"
setup_dict["date_col"] = "开始日期"
setup_dict["coil_len_col"] = "热卷长度"
setup_dict["aim_thick_col"] = "目标厚度"
setup_dict["aim_fdt_col"] = "轧机出口目标温度"
setup_dict["aim_ct_col"] = "热卷卷曲目标温度"
setup_dict["aim_c40_col"] = "目标凸度"

# columns dump in English
setup_dict["coil_id_col"] = "coil_id"
setup_dict["date_col"] = "start_date"
setup_dict["coil_len_col"] = "coil_len"
setup_dict["aim_thick_col"] = "aim_thick"
setup_dict["aim_fdt_col"] = "aim_fdt"
setup_dict["aim_ct_col"] = "aim_ct"
setup_dict["aim_c40_col"] = "aim_c40"

result_dir = os.path.join(root_dir, origin_result_dir)
setup_dict["result_dir"] = result_dir

print(setup_dict)
pondo(setup_dict)
