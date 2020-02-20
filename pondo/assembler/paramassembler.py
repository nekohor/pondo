from rollen.utils import DirectoryUtils

from .assembler_coil_info import CoilInfoAssembler
from .assembler_func_option import FuncOptionAssembler
from .assembler_length_mode import LengthModeAssembler


class ParamAssembler:

    def __init__(self, assem_type):

        self.assem_type = assem_type

    def get_rule(self):
        return self.rule

    def set_rule(self, rule):
        self.rule = rule

    def get_record(self):
        return self.record

    def set_record(self, record):
        self.record = record

    def check_attribute(self):

        attributes = ["rule", "record"]

        for attribute in attributes:
            if not hasattr(self, attribute):
                raise AttributeError("{} doesnt exist".format(attribute))

    def get_params(self):
        self.check_attribute()
        if self.assem_type == "stat":
            params = self.assem_stat_params()
        elif self.assem_type == "export":
            params = self.assem_export_params()
        else:
            raise Exception("wrong assemble type")
        return params

    def assem_stat_params(self):

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

    def assem_export_params(self):

        params = {}

        ci_assem = CoilInfoAssembler(self.rule, self.record)
        params["coilId"] = ci_assem.get_coil_id()
        params["curDir"] = ci_assem.get_cur_dir()
        params["factorNames"] = ci_assem.get_factor_name()

        return params
