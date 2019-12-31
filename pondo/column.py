import numpy as np


class ColumnName():

    def __init__(self, rule):
        self.rule = rule

    def get_base_col(self):
        return "_".join([
            self.rule.get_segment_name(),
            self.rule.get_factor_name(),
            self.rule.get_func_name()
        ])

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

    def get_col(self):
        col = self.get_base_col()

        if self.has_func_options():
            col = col + "_" + self.get_func_option_tag()

        return col.upper()

    def get_func_option_tag(self):
        if np.isnan(self.rule.get_lower()) & np.isnan(self.rule.get_upper()):
            return self.get_tolerance_tag()
        else:
            lower = self.cut_tail(self.rule.get_lower())
            upper = self.cut_tail(self.rule.get_upper())
            return lower + "_" + upper

    def get_tolerance_tag(self):
        if np.isnan(self.rule.get_tol_perc()):
            return self.get_raw_tol_tag()
        else:
            return self.get_thick_perc_tol_tag()

    def get_raw_tol_tag(self):
        return self.cut_tail(self.convert_unit(self.rule.get_tol()))

    def get_thick_perc_tol_tag(self):
        tol_perc = self.cut_tail(self.rule.get_tol_perc())
        tol_max = self.cut_tail(self.convert_unit(self.rule.get_tol_max()))

        tol_tag = "_".join([
            "thk{}%".format(tol_perc),
            "max{}".format(tol_max)
        ])

        return tol_tag

    def convert_unit(self, tol):
        if (self.rule.get_unit() == "mm") & (self.rule.get_tol() < 1):
            coverted_tol = tol * 1000
        else:
            coverted_tol = tol
        return str(coverted_tol)

    def cut_tail(self, tag_component):
        component = str(tag_component)
        if component[-2:] == ".0":
            return component[: -2]
        else:
            return component
