from pondo2 import pondo
import configparser
import os

conf = configparser.ConfigParser()
conf_filename = "luna.conf"
conf.read(conf_filename, encoding="utf-8-sig")

line = conf.getint("configure", "line")
month = conf.get("configure", "month")
item = conf.get("configure", "item")

origin_root_dir = conf.get("path", "root_dir")
origin_result_dir = conf.get("path", "result_dir")
result_dir = os.path.join(origin_root_dir, origin_result_dir)

if conf_filename == "luna.conf":
    root_dir = os.path.join(origin_root_dir, str(line), month)
    coil_id_table_filename = '{}_{}{}.xlsx'.format(month, line, item)
else:
    root_dir = root_dir
    coil_id_table_filename = conf.get("path", "coil_id_table_filename")

setup_dict = {}
setup_dict["line"] = line
setup_dict["root_dir"] = root_dir
setup_dict["coil_id_table_filename"] = coil_id_table_filename
setup_dict["data_dir"] = conf.get("drive_id", "{}_drive".format(line))
setup_dict["coil_id_col"] = conf.get("configure", "coil_id_col")
setup_dict["date_col"] = conf.get("configure", "date_col")
setup_dict["result_dir"] = result_dir

print(setup_dict)
pondo(setup_dict)
