from solders import keypair, pubkey
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import Message
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from sol_interface.requests.buy import TokensBuyRequest
from sol_interface.requests.quote import TransactionQuoteRequest
from sol_interface.requests.transaction import TransactionRequest


class Wallet:
    def __init__(self, key_pair: keypair.Keypair,
                 quote_request: TransactionQuoteRequest,
                 transaction_request: TransactionRequest,
                 buy_transaction_request: TokensBuyRequest):
        self.__key_pair = key_pair
        self.__quote_request = quote_request
        self.__transaction_request = transaction_request
        self.__buy_transaction_request = buy_transaction_request

    @property
    def public_key(self) -> Pubkey:
        return self.__key_pair.pubkey()

    @property
    def private_key(self) -> Keypair:
        return self.__key_pair

    def send_sol(self, account_to: pubkey.Pubkey, count_lamports: int, blockhash: Hash) -> Transaction:
        instruction = transfer(TransferParams(from_pubkey=self.__key_pair.pubkey(),
                                              to_pubkey=account_to,
                                              lamports=count_lamports))
        message = Message(payer=self.__key_pair.pubkey(), instructions=[instruction])
        return Transaction([self.__key_pair], message, blockhash)

    def buy_token(self, token: str, amount: int, fee: int) -> str:
        solana_hex = "So11111111111111111111111111111111111111112"
        quote = self.__quote_request.request(solana_hex, token, amount)
        key = str(self.__key_pair.pubkey())
        instruction_string: str = self.__transaction_request.request(fee, quote, key, True)["transaction"]
        self.__buy_transaction_request.request(instruction_string, str(self.__key_pair))
