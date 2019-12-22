from pondo3 import pondo
import configparser
import os

conf = configparser.ConfigParser()
config_dir = "config"
conf_filename = "luna.conf"
config_path = os.path.join(config_dir, conf_filename)
conf.read(config_path, encoding="utf-8-sig")

line = conf.getint("configure", "line")

origin_root_dir = conf.get("path", "root_dir")
origin_result_dir = conf.get("path", "result_dir")


if conf_filename == "luna.conf":
    month = conf.get("configure", "month")
    item = conf.get("configure", "item")
    root_dir = os.path.join(origin_root_dir, str(line), month)
    coil_id_table_name = '{}_{}{}.xlsx'.format(month, line, item)
else:
    root_dir = origin_root_dir
    coil_id_table_name = conf.get("path", "coil_id_table_name")


setup_dict = {}
setup_dict["line"] = line
setup_dict["root_dir"] = root_dir
setup_dict["coil_id_table_name"] = coil_id_table_name
setup_dict["task_table_name"] = conf.get("path", "task_table_name")
setup_dict["data_dir"] = conf.get("drive_id", "{}_drive".format(line))
setup_dict["coil_id_col"] = conf.get("columns", "coil_id_col")
setup_dict["date_col"] = conf.get("columns", "date_col")
setup_dict["coil_len_col"] = conf.get("columns", "coil_len_col")
setup_dict["aim_thick_col"] = conf.get("columns", "aim_thick_col")
setup_dict["aim_fdt_col"] = conf.get("columns", "aim_fdt_col")
setup_dict["aim_ct_col"] = conf.get("columns", "aim_ct_col")
setup_dict["aim_c40_col"] = conf.get("columns", "aim_c40_col")

result_dir = os.path.join(root_dir, origin_result_dir)
setup_dict["result_dir"] = result_dir

print(setup_dict)
pondo(setup_dict)
