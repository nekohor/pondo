import requests
import json
from rollen.config.url import POND_API_URL
from rollen.config.url import EXPORTS_API_URL
from rollen.config.url import STATS_API_URL


class Client():

    def __init__(self):
        pass

    def send_request(self, req_type, params):

        self.req_type = req_type
        self.params = params
        self.coil_id = params["coilId"]

    def get_api_url(self):

        if self.req_type == "exports":
            api_url = EXPORTS_API_URL

        elif self.req_type == "stats":
            api_url = STATS_API_URL
        else:
            raise Exception("Unmatched request type in client")

        return api_url

    def get_response(self):

        request_api_url = self.get_api_url() + "/" + self.coil_id

        response = requests.get(request_api_url, params=self.params)

        self.raw_url = response.url

        print(response.text)
        return json.loads(response.text).get(self.req_type)
