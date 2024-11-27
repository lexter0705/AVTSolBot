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

    def send_sol(self, account_to: pubkey.Pubkey, count_lamports: int) -> VersionedTransaction:
        instruction = transfer(TransferParams(from_pubkey=self.__key_pair.pubkey(),
                                              to_pubkey=account_to,
                                              lamports=count_lamports))
        blockhash = Hash.default()
        message = MessageV0.try_compile(
            payer=self.__key_pair.pubkey(),
            instructions=[instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash
        )
        return VersionedTransaction(message, [self.__key_pair])

    def buy_token(self, token: str, amount: int) -> VersionedTransaction:
        solana_hex = "So11111111111111111111111111111111111111112"
        quote = self.__quote_request.request(solana_hex, token, amount)
        transaction = bytes(self.__transaction_request.request(100, quote, str(self.__key_pair.pubkey()), False))
        return VersionedTransaction.from_bytes(transaction)

    def get_pubkey(self):
        return self.__key_pair.pubkey()
