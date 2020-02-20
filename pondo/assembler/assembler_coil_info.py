from rollen.utils.millline import MillLine
from rollen.utils import DirectoryUtils


class CoilInfoAssembler():

    def __init__(self, rule, record):

        self.rule = rule
        self.record = record

    def get_coil_id(self):
        return self.record["coil_id"]

    def get_factor_name(self):
        if type(self.rule) == str:
            return self.rule
        else:
            return self.rule.get_factor_name()

    def get_date(self):
        return self.record["start_date"]

    def get_cur_dir(self):
        return self.record["cur_dir"]
