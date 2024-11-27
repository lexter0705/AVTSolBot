from sol_interface.requests.abstract_request import Request
import requests


class TransactionRequest(Request):
    def __init__(self, link: str):
        super().__init__(link)

    def request(self, priority_fee_lamports: int, quote: dict, public_key: str,
                warp_and_unwrap_sol: bool) -> dict:
        data = {"priorityFeeLamports": priority_fee_lamports, "quote": quote, "userPublicKey": public_key,
                "warpAndUnwrapSol": warp_and_unwrap_sol}
        response = requests.post(self.get_link(), data=data)
        return response.json()
