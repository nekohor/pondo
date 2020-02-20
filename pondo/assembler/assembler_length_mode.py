import rollen


class LengthModeAssembler():

    def __init__(self, rule, record):

        self.rule = rule
        self.record = record

        self.conf = rollen.registry.get_config("lengthMode")

        self.has_head_tail_perc = False
        self.has_head_tail_len = False

        self.build_length_params()
        self.build_cut_params()

    def get_segment_name(self):
        return self.rule.get_segment_name()

    def get_length_mode(self):
        return self.rule.get_length_mode()

    def build_length_params(self):

        length_mode = self.get_length_mode().lower()

        if length_mode == "average":
            self.head_perc = self.conf["length"][length_mode]["headPerc"]
            self.tail_perc = self.conf["length"][length_mode]["tailPerc"]
            self.has_head_tail_perc = True
        elif length_mode == "bite":
            self.head_len = self.conf["length"][length_mode][
                self.record["line"]]["headLen"]
            self.tail_len = self.conf["length"][length_mode][
                self.record["line"]]["tailLen"]
            self.has_head_tail_len = True
        else:
            self.head_len = self.conf["length"][length_mode]["headLen"]
            self.tail_len = self.conf["length"][length_mode]["tailLen"]
            self.has_head_tail_len = True

    def build_cut_params(self):

        factor_name = self.rule.get_factor_name()
        line = self.record["line"]

        if factor_name == "r2dt":
            self.head_cut = self.conf["cut"]["r2dt"][line]["headCut"]
            self.tail_cut = self.conf["cut"]["r2dt"][line]["tailCut"]
        else:
            self.head_cut = self.conf["cut"]["normal"]["headCut"]
            self.tail_cut = self.conf["cut"]["normal"]["tailCut"]

    def get_head_perc(self):
        return self.head_perc

    def get_tail_perc(self):
        return self.tail_perc

    def get_head_len(self):
        return self.head_len

    def get_tail_len(self):
        return self.tail_len

    def get_head_cut(self):
        return self.head_cut

    def get_tail_cut(self):
        return self.tail_cut
