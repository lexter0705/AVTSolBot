from config import json_checker
from sol_interface.requests.abstract_request import Request
import requests


class TransactionRequest(Request):
    def __init__(self):
        self.__link = json_checker.get_data()["get_transaction_link"]

    def request(self, priority_fee_lamports: int, quote: dict, public_key: str,
                warp_and_unwrap_sol: bool) -> dict:
        data = {"priorityFeeLamports": priority_fee_lamports, "quote": quote, "userPublicKey": public_key,
                "warpAndUnwrapSol": warp_and_unwrap_sol}
        response = requests.post(self.__link, data=data)
        return response.json()
