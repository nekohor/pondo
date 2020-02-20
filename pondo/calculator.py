import numpy as np
import pandas as pd


class Calculator():

    def __init__(self, response, params):

        self.response = response
        self.params = params

        self.coil_id = self.params["coilId"]
        self.factor_name = self.params["factorName"]

        self.function_name = self.params["functionName"]
        self.unit = self.params["unit"]

        self.length_name = self.params["lengthName"]
        self.head_cut = self.params["headCut"]
        self.tail_cut = self.params["tailCut"]

        try:
            self.data = pd.Series(
                self.response["factors"][self.factor_name]["data"])
        except KeyError:
            self.data = pd.Series([])

        self.data_size = len(self.data)

    def get_head_tail_len(self):

        keys = self.params.keys()

        if ("headPerc" in keys) & ("tailPerc" in keys):
            head_len = self.data_size * self.params["headPerc"]
            tail_len = self.data_size * self.params["tailPerc"]
        elif ("headLen" in keys) & ("tailLen" in keys):
            head_len = self.params["headLen"]
            tail_len = self.params["tailLen"]
        else:
            head_len = 0
            tail_len = 0

        return head_len, tail_len

    def get_length_index(self):

        head_cut, tail_cut = self.head_cut, self.tail_cut
        head_len, tail_len = self.get_head_tail_len()

        segment = self.length_name
        size = self.data_size

        if segment == "head":
            start = head_cut
            end = head_len + head_cut
        elif segment == "middle":
            start = head_len + head_cut
            end = size - tail_len - tail_cut
        elif segment == "tail":
            start = size - tail_len - tail_cut
            end = size - tail_cut
        elif segment == "body":
            start = head_len + head_cut
            end = size - tail_cut
        elif segment == "main":
            start = head_cut
            end = size - tail_cut
        elif segment == "total":
            start = 0
            end = size
        elif segment == "first":
            start = head_cut
            end = head_cut + 5
        else:
            raise Exception("Unmatched segment name in Calculator")
        return int(start), int(end)

    def calculate(self):

        start_idx, end_idx = self.get_length_index()
        array = self.data[start_idx:end_idx]

        if array.shape[0] == 0:
            result = np.nan

        func_name = self.function_name.lower()
        if func_name == "aimrate":
            result = self.calc_aimrate(array)
        elif func_name == "stability":
            result = self.calc_stability(array)
        elif func_name == "pickwedge":
            result = self.calc_pickwedge(array)
        elif func_name == "max":
            result = np.max(array)
        elif func_name == "absmax":
            result = np.max(np.abs(array))
        elif func_name == "min":
            result = np.min(array)
        elif func_name == "std":
            result = np.std(array)
        elif func_name == "mean":
            result = np.mean(array)
        elif func_name == "absmean":
            result = np.mean(np.abs(array))
        elif func_name == "sum":
            result = np.sum(array)
        elif func_name == "abssum":
            result = np.sum(np.abs(array))
        else:
            raise Exception("Unmatched stat func name")

        if type(result) == str:
            return result
        else:
            return round(result, 3)

    def get_upper_lower(self):

        keys = self.params.keys()

        if ("upper" in keys) & ("lower" in keys):
            upper = self.params["upper"]
            lower = self.params["lower"]
        elif ("aim" in keys) & ("tolerance" in keys):
            aim = self.params["aim"]
            tol = self.params["tolerance"]
            upper = aim + tol
            lower = aim - tol
        else:
            upper = 0
            lower = 0
        return self.convert_unit(upper), self.convert_unit(lower)

    def convert_unit(self, val):

        if self.unit == "um":
            converted = val / 1000
        else:
            converted = val

        return converted

    def calc_aimrate(self, array):
        upper, lower = self.get_upper_lower()
        return array.apply(
            lambda x: 1 if (x >= lower) & (x <= upper) else 0).mean() * 100

    def calc_stability(self, array):
        tol = self.params["tolerance"]
        aim = np.mean(array)
        upper = aim + tol
        lower = aim - tol
        return array.apply(
            lambda x: 1 if (x >= lower) & (x <= upper) else 0).mean() * 100

    def calc_pickwedge(self, array):
        mid = int(len(array) / 2)
        cut = 45
        tol = 0.02
        first_child = array[cut: mid - 1]
        second_child = array[mid: -cut]

        if np.max(first_child) - np.min(first_child) <= tol:
            first_pass = 1
        else:
            first_pass = 0

        if np.max(second_child) - np.min(second_child) <= tol:
            second_pass = 1
        else:
            second_pass = 0

        return "{}|{}".format(first_pass, second_pass)
