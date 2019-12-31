import datetime
import os


class Saver():

    def __init__(self, task_name):

        self.task_name = task_name

    def save_batch_stat(self, df, line, start_date, end_date):
        filename = self.get_batch_stat_filename(line, start_date, end_date)
        df.to_excel(filename)

    def save_stat(self, df, dir_name):
        filename = self.get_stat_filename(dir_name)
        df.to_excel(filename)

    def get_save_dir(self, dir_name):
        save_dir = "E:/stat_result" + "/" + dir_name
        if os.path.exists(save_dir):
            os.makedirs(save_dir)
        return save_dir

    def get_batch_stat_filename(self, line, start_date, end_date):
        filename = "stat_{}_{}_{}_{}.xlsx".format(
            line, self.task_name, start_date, end_date)
        return self.get_save_dir("batch") + "/" + filename

    def get_stat_filename(self, dir_name):
        timenow = datetime.datetime.now()
        time_tag = timenow.strftime("%Y%m%d_%H%M%S")
        filename = "stat_{}_{}.xlsx".format(self.task_name, time_tag)
        return self.get_save_dir(dir_name) + "/" + filename
