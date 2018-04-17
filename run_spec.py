from pond_reader import pondo
from pond_reader import pondo_total


drive_id = {"1580": "i", "2250": "h"}

line = 2250
# month = 201803
root_dir = "e:/005统计/20180417_lyl统计分析"

setup_dict = {
    "line": line,
    "data_dir": "{}:/{}hrm".format(drive_id[str(line)], line),
    "coil_id_col": "热卷号",
    "product_date_col": "开始日期",
    "coil_id_table_filename": root_dir + "/厚度命中率.xlsx",
    "result_dir": root_dir + "/lyl_indicator.xlsx"
}

pondo(**setup_dict)
