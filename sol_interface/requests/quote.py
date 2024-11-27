import requests
from sol_interface.requests.abstract_request import Request


class TransactionQuoteRequest(Request):
    def __init__(self, link):
        super().__init__(link)

    def request(self, input_token: str, output_token: str, amount: int) -> dict:
        response = requests.post(self.get_link(), data={"inputMint": input_token, "amount": amount,
                                                    "outputMint": output_token})
        return response.json()