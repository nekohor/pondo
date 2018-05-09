from pondo2 import pondo


drive_id = {"1580": "i", "2250": "h"}

line = 2250
root_dir = "e:/005统计/20180417_lyl统计分析"

setup_dict = {
    "line": line,
    "coil_id_table_filename": root_dir + "/厚度命中率.xlsx",
    "data_dir": "{}:/{}hrm".format(drive_id[str(line)], line),
    "coil_id_col": "热卷号",
    "date_col": "开始日期",
    "aim_col": None,
    "result_dir": root_dir + "/lyl_indicator.xlsx"
}

pondo(setup_dict)
