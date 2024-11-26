from urllib.request import Request

import requests
from config import json_checker
from sol_interface.requests.abstract_request import Request


class TransactionQuoteRequest(Request):
    def __init__(self):
        self.__link = json_checker.get_data()["get_quote_link"]

    def request(self, input_token: str, output_token: str, amount: int) -> dict:
        response = requests.post(self.__link, data={"inputMint": input_token, "amount": amount,
                                                    "outputMint": output_token})
        return response.json()