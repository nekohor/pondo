import requests
import json
import socket

from rollen.config.url import EXPORT_API_URL
from rollen.config.url import STAT_API_URL


class HttpClient():

    def __init__(self):
        pass

    def send_request(self, req_type, params):

        self.req_type = req_type
        self.params = params
        self.coil_id = params["coilId"]

    def get_api_url(self):

        if self.req_type == "export":
            api_url = EXPORT_API_URL
        elif self.req_type == "stat":
            api_url = STAT_API_URL
        else:
            raise Exception("Unmatched request type in client")

        return api_url

    def get_response(self):

        request_api_url = self.get_api_url() + "/" + self.coil_id

        response = requests.get(request_api_url, params=self.params)

        self.raw_url = response.url

        return json.loads(response.text).get(self.req_type)


class TcpClient():

    def __init__(self):
        pass

    def send_request(self, params):

        req = {}
        req["request"] = params
        self.req = json.dumps(req)

    def get_response(self):

        client = socket.socket()
        # 连接到localhost主机的8999端口上去
        client.connect(('localhost', 8999))

        # 把编译成utf-8的数据发送出去
        client.send(self.req.encode('utf-8'))

        # 接收数据
        resp = client.recv(10000000)
        resp_dict = json.loads(resp.decode())
        client.close()

        return resp_dict
