from config.millline import HRM_TAG_LIST
from pondo.utils.millline import MillLine
from pondo.dao.pond.directory import DirectoryDao
import os


class DirectoryService():

    def sync(self):

        for line_tag in HRM_TAG_LIST:

            root_dir = MillLine.get_pond_root_dir(line_tag)
            months = os.listdir(root_dir)

            for month in months:

                month_dir = root_dir + "/" + month
                dates = os.listdir(month_dir)

                for date in dates:

                    d = DirectoryDao(line_tag)
                    # d.create_all_table()
                    d.sync_table_with_date(date)

                    print(date， "sync complete")
