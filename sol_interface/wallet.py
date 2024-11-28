from solders import keypair, pubkey
from solders.hash import Hash
from solders.message import MessageV0, Message
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction, Transaction
from sol_interface.requests.quote import TransactionQuoteRequest
from sol_interface.requests.transaction import TransactionRequest


class Wallet:
    def __init__(self, key_pair: keypair.Keypair,
                 quote_request: TransactionQuoteRequest,
                 transaction_request: TransactionRequest):
        self.__key_pair = key_pair
        self.__quote_request = quote_request
        self.__transaction_request = transaction_request

    def send_sol(self, account_to: pubkey.Pubkey, count_lamports: int, blockhash: Hash) -> Transaction:
        instruction = transfer(TransferParams(from_pubkey=self.__key_pair.pubkey(),
                                              to_pubkey=account_to,
                                              lamports=count_lamports))
        message = Message(payer=self.__key_pair.pubkey(), instructions=[instruction])
        return Transaction([self.__key_pair], message,  blockhash)

    def buy_token(self, token: str, amount: int, fee: int) -> Transaction:
        solana_hex = "So11111111111111111111111111111111111111112"
        quote = self.__quote_request.request(solana_hex, token, amount)
        transaction = bytes(self.__transaction_request.request(fee, quote, str(self.__key_pair.pubkey()), False))
        return Transaction.from_bytes(transaction)

    @property
    def public_key(self):
        return self.__key_pair.pubkey()
