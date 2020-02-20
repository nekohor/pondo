import numpy as np


class FuncOptionAssembler():

    def __init__(self, rule, record):

        self.rule = rule
        self.record = record

        self.has_tolerance = False
        self.has_upper_lower = False

        if self.has_func_options():
            self.build_func_options()

    def has_func_options(self):

        no_upper = np.isnan(self.rule.get_upper())
        no_lower = np.isnan(self.rule.get_lower())

        # no_aim = np.isnan(self.rule.get_aim())
        no_tol = np.isnan(self.rule.get_tol())
        no_tol_perc = np.isnan(self.rule.get_tol_perc())
        no_tol_max = np.isnan(self.rule.get_tol_max())

        if no_upper & no_lower & no_tol & no_tol_perc & no_tol_max:
            return False
        else:
            return True

    def get_func_name(self):
        return self.rule.get_func_name()

    def get_unit(self):
        return self.rule.get_unit()

    def build_func_options(self):

        upper = self.rule.get_upper()
        lower = self.rule.get_lower()

        if np.isnan(upper) & np.isnan(lower):
            self.build_tolerance()
            self.has_tolerance = True
        else:
            self.upper = upper
            self.lower = lower
            self.has_upper_lower = True

    def build_tolerance(self):
        self.aim = self.get_aim()
        self.tol = self.get_tol()

    def get_aim(self):

        aim = self.rule.get_aim()

        if type(aim) == str:
            return self.record["aim_{}".format(aim)]
        elif np.isnan(aim):
            return np.nan
        else:
            return aim

    def get_tol(self):

        tol = self.rule.get_tol()
        tol_prec = self.rule.get_tol_perc()

        if not np.isnan(tol_prec):
            return self.get_tol_by_thk()
        else:
            return tol

    def get_tol_by_thk(self):

        tol_prec = self.rule.get_tol_perc()
        tol_max = self.rule.get_tol_max()

        tol = tol_prec / 100 * self.record["aim_thick"]
        return np.minimum(tol, tol_max)

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower
