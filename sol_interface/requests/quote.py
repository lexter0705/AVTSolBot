import requests
from sol_interface.requests.abstract_request import Request


class TransactionQuoteRequest(Request):
    def __init__(self, link):
        super().__init__(link)

    def request(self, input_token: str, output_token: str, amount: int) -> dict:
        request_stroke = f"?inputMint={input_token}&outputMint={output_token}&amount={amount}"
        response = requests.get(self.link+request_stroke)
        return response.json()
