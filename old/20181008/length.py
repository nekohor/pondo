

class Length():

    def __init__(self, line, rule, coil_len):
        self.line
        self.rule = rule
        self.build_hdtl(coil_len)
        self.build_cut()

    def build_cut(self):
        self.head_cut = 5
        self.tail_cut = 5

    def build_hdtl(self, coil_len):
        if self.rule["LENGTH_MODE"] == "bite":
            self.build_bite()
        elif self.rule["LENGTH_MODE"] == "feedback":
            self.build_feedback()
        elif self.rule["LENGTH_MODE"] == "average":
            self.build_average(coil_len)

    def build_bite(self):
        if 1580 == self.line:
            self.head_len = 120
            self.tail_len = 50
        elif 2250 == self.line:
            self.head_len = 150
            self.tail_len = 50
        else:
            raise Exception("wrong line")

    def build_feedback(self):
        self.head_len = 50
        self.tail_len = 50

    def build_average(self, coil_len):
        self.head_len = coil_len * 0.333
        self.tail_len = coil_len * 0.333

    def get_head_len(self):
        return self.head_len

    def get_tail_len(self):
        return self.tail_len

    def get_head_cut(self):
        return self.head_cut

    def get_tail_cut(self):
        return self.tail_cut

hdtl = Length(self.line, record)
schema_dict["head_len"] = hdtl.get_head_len()
schema_dict["tail_len"] = hdtl.get_tail_len()
schema_dict["head_cut"] = hdtl.get_head_cut()
schema_dict["tail_cut"] = hdtl.get_tail_cut()
schema_dict["stat_name"] = record["STAT_FN"]
schema_dict["seg_name"] = record["SEGMENT"]
