from pondo.database import DataBaseManager


class CurveDao():

    def __init__(self):

        self.conn = DataBaseManager.get_database("qms")

    def get_data(self):
        pass
