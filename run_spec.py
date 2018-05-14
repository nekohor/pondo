from pondo2 import pondo


drive_id = {"1580": "i", "2250": "h"}

line = 2250
root_dir = "e:/005统计/20180511_M610L浪形预报统计"

setup_dict = {
    "line": line,
    "root_dir": root_dir,
    "coil_id_table_filename": "M610L.xlsx",
    "data_dir": "{}:/{}hrm".format(drive_id[str(line)], line),
    "coil_id_col": "热卷号",
    "date_col": "开始日期",
    "result_dir": root_dir + "/预报数据.xlsx"
}

pondo(setup_dict)
