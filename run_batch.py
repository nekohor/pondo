from pondo2 import pondo_total_batch


drive_id = {"1580": "i", "2250": "h"}

line = 1580
month = 201803
root_dir = "d:/data_collection_monthly/{}/{}".format(line, month)
item = "excel_test"

setup_dict = {
    "line": line,
    "coil_id_table_filename": '{}_{}{}.xlsx'.format(month, line, item),
    "data_dir": "{}:/{}hrm".format(drive_id[str(line)], line),
    "coil_id_col": "热卷号",
    "date_col": "开始日期",
    "result_dir": root_dir + "/test_result"
}

pondo_total_batch(setup_dict)
