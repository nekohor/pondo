from config.millline import HRM1580_POND_ROOT_DIR
from config.millline import HRM2250_POND_ROOT_DIR
from config.millline import HRM2250_TAG
from config.millline import HRM1580_TAG
from config.millline import HRM2250_COILID_HEADER
from config.millline import HRM1580_COILID_HEADER


class WrongMillLineError(Exception):
    pass


class MillLine():

    # def __init__(self, line_tag):
    #     self.line_tag = line_tag

    @classmethod
    def get_coil_id_header(cls, line_tag):

        if line_tag == HRM2250_TAG:
            return HRM2250_COILID_HEADER
        if line_tag == HRM1580_TAG:
            return HRM1580_COILID_HEADER

        raise WrongMillLineError(
            "line_tag matches wrong in get_coil_id_header")

    @classmethod
    def get_line_by_id(cls, coil_id):

        if type(coil_id) != str:
            raise WrongMillLineError("coilId is not a string")

        coil_id_header = coil_id[0]

        if coil_id_header == HRM2250_COILID_HEADER:
            return HRM2250_TAG
        if coil_id_header == HRM1580_COILID_HEADER:
            return HRM1580_TAG

        raise WrongMillLineError("line_tag matches wrong in get_line_by_id")

    @classmethod
    def get_pond_root_dir(cls, line_tag):

        if line_tag == HRM2250_TAG:
            return HRM2250_POND_ROOT_DIR
        if line_tag == HRM1580_TAG:
            return HRM1580_POND_ROOT_DIR

        raise WrongMillLineError("line_tag matches wrong for pond root dir")
