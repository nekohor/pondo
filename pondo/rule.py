
class Rule():

    def __init__(self, rule):
        self.rule = rule

    def get_segment_name(self):
        return self.rule["SEGMENT"]

    def get_factor_name(self):
        return self.rule["FACTOR"]

    def get_func_name(self):
        return self.rule["FUNC"]

    def get_aim(self):
        return self.rule["AIM"]

    def get_tol(self):
        return self.rule["TOL"]

    def get_tol_perc(self):
        return self.rule["TOL_PERC"]

    def get_tol_max(self):
        return self.rule["TOL_MAX"]

    def get_upper(self):
        return self.rule["UPPER"]

    def get_lower(self):
        return self.rule["LOWER"]

    def get_unit(self):
        return self.rule["UNIT"]

    def get_length_mode(self):
        return self.rule["LENGTH_MODE"]
