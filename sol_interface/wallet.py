from solders import keypair, pubkey
from solders.hash import Hash
from solders.message import MessageV0
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction

from sol_interface.requests.quote import TransactionQuoteRequest
from sol_interface.requests.transaction import TransactionRequest


class Wallet:
    def __init__(self, key_pair: keypair.Keypair,
                 quote_request: TransactionQuoteRequest,
                 transaction_request: TransactionRequest):
        self.__key_pair = key_pair
        self.__quote_request = quote_request
        self.__transaction_request = transaction_request

    def get_balance(self) -> int:
        pass

    def send_sol(self, account_to: pubkey.Pubkey):
        instruction = transfer(TransferParams(from_pubkey=self.__key_pair.pubkey(),
                                              to_pubkey=account_to,
                                              lamports=self.get_balance()))
        blockhash = Hash.default()
        message = MessageV0.try_compile(
            payer=self.__key_pair.pubkey(),
            instructions=[instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash
        )
        VersionedTransaction(message, [self.__key_pair])

    def buy_token(self, token: str, amount: int):
        pass

    def get_pubkey(self):
        return self.__key_pair.pubkey()