import requests
from config.api import POND_API_URL


class ApiServer():

    @staticmethod
    def run():
        params = {
            # "factorNames": ",".join(["wedge40", "crown40", "thick_clg", "width_mfg"]),
            "factorNames": ",".join(["wedge40"]),
            "curDir": "E:/2250hrm/201911/20191108"
        }
        request_api_url = POND_API_URL + "/" + "H19148841L"
        response = requests.get(request_api_url, params=params)
        print(response.text)
        print(response.url)
