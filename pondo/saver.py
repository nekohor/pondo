import datetime
import os


class Saver():

    def __init__(self, task_name):

        self.task_name = task_name

    def get_save_dir(self, req_type, dir_name, sub_dir_name=""):
        save_dir = "E:/{}_result/{}".format(req_type, dir_name)

        if sub_dir_name != "":
            save_dir = save_dir + "/" + sub_dir_name

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        return save_dir

    def get_time_tag(self):
        time_tag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return time_tag
    # about stats

    def save_batch_stat(self, df, line, start_date, end_date):
        filename = self.get_batch_stat_filename(line, start_date, end_date)
        filepath = self.get_save_dir("stats", "batch") + "/" + filename
        df.to_excel(filepath)

    def save_stat(self, df, dir_name):
        filename = self.get_stat_filename(dir_name)
        filepath = self.get_save_dir("stats", dir_name) + "/" + filename
        df.to_excel(filepath)

    def get_batch_stat_filename(self, line, start_date, end_date):
        filename = "stat_{}_{}_{}_{}.xlsx".format(
            self.task_name, line, start_date, end_date)
        return filename

    def get_stat_filename(self, dir_name):
        filename = "stat_{}_{}.xlsx".format(
            self.task_name, self.get_time_tag())
        return filename

    # about exports

    def get_batch_export_filename(
            self, line, start_date, end_date):

        filename = "exports_{}_{}_{}_{}.xlsx".format(
            self.task_name, line, start_date, end_date)

        return filename

    def get_batch_export_filepath(
            self, line, start_date, end_date):

        sub_dir_name = "exports_{}_{}_{}".format(
            line, start_date, end_date)

        filename = self.get_batch_export_filename(line, start_date, end_date)

        filepath = self.get_save_dir(
            "exports", "batch", sub_dir_name) + "/" + filename

        return filepath

    def get_export_filepath(self, dir_name):

        time_tag = self.get_time_tag()

        sub_dir_name = "exports_{}".format(time_tag[:6])

        filename = "exports_{}_{}.xlsx".format(
            self.task_name, time_tag)

        filepath = self.get_save_dir(
            "exports", dir_name, sub_dir_name) + "/" + filename

        return filepath
