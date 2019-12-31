from rollen.utils import DirectoryUtils

from .assem_coil_info import CoilInfoAssembler
from .assem_func_option import FuncOptionAssembler
from .assem_length_mode import LengthModeAssembler


class Assembler:

    def __init__(self, assem_type):

        self.assem_type = assem_type

    def set_rule(self, rule):

        self.rule = rule

    def set_record(self, record):

        self.record = record

    def check_attribute(self):

        attributes = ["rule", "record"]

        for attribute in attributes:
            if not hasattr(self, attribute):
                raise AttributeError("{} doesnt exist".format(attribute))

    def get_params(self):
        self.check_attribute()
        params = getattr(self, "assem_{}_params".format(self.assem_type))()
        return params

    def assem_stats_params(self):

        params = {}

        ci_assem = CoilInfoAssembler(self.rule, self.record)
        params["coilId"] = ci_assem.get_coil_id()
        params["curDir"] = ci_assem.get_cur_dir()
        params["factorName"] = ci_assem.get_factor_name()

        fo_assem = FuncOptionAssembler(self.rule, self.record)
        params["functionName"] = fo_assem.get_func_name()
        params["unit"] = fo_assem.get_unit()
        if fo_assem.has_func_options():
            if fo_assem.has_tolerance:
                params["aim"] = fo_assem.get_aim()
                params["tolerance"] = fo_assem.get_tol()
            if fo_assem.has_upper_lower:
                params["upper"] = fo_assem.get_upper()
                params["lower"] = fo_assem.get_lower()

        lm_assem = LengthModeAssembler(self.rule, self.record)
        params["lengthName"] = lm_assem.get_segment_name()
        if lm_assem.has_head_tail_perc:
            params["headPerc"] = lm_assem.get_head_perc()
            params["tailPerc"] = lm_assem.get_tail_perc()
        if lm_assem.has_head_tail_len:
            params["headLen"] = lm_assem.get_head_len()
            params["tailLen"] = lm_assem.get_tail_len()

        params["headCut"] = lm_assem.get_head_cut()
        params["tailCut"] = lm_assem.get_tail_cut()

        return params

    def assem_exports_params(self):

        params = {}

        ci_assem = CoilInfoAssembler(self.rule, self.record)
        params["coilId"] = ci_assem.get_coil_id()
        params["curDir"] = ci_assem.get_cur_dir()
        params["factorNames"] = ci_assem.get_factor_name()

        return params
