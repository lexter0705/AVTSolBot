from solders.keypair import Keypair
from sol_interface.requests.quote import TransactionQuoteRequest
from sol_interface.requests.transaction import TransactionRequest
from sol_interface.wallet import Wallet


class WalletConverter:
    def __init__(self, quote: TransactionQuoteRequest, transaction: TransactionRequest):
        self.__quote = quote
        self.__transaction = transaction

    def from_private_key(self, private_key: str) -> Wallet:
        keypair = Keypair.from_base58_string(private_key)
        wallet = Wallet(keypair, self.__quote, self.__transaction)
        return wallet