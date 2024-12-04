import requests
from sol_interface.requests.abstract_request import Request


class TokensBuyRequest(Request):
    def __init__(self, rpc_url: str, link_to_request: str):
        super().__init__(link_to_request)
        self.__rpc_url = rpc_url

    def request(self, transaction: str, private_key: str):
        data = {"userPrivateKey": private_key, "transactionHex": transaction, "rpcLink": self.__rpc_url}
        requests.post(self.link, json=data)
