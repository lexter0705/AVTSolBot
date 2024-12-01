from functools import singledispatchmethod
from solana.rpc.async_api import AsyncClient
from sol_interface import Wallet, Wallets


class StringsFormer(object):
    def __init__(self, client: AsyncClient):
        self.__client = client

    @singledispatchmethod
    async def form_string(self, wallet: Wallet | Wallets) -> str:
        pass

    @form_string.register(Wallet)
    async def _(self, wallet: Wallet) -> str:
        public_key = wallet.private_key.pubkey()
        private_key = wallet.private_key
        balance = (await self.__client.get_balance(public_key)).value / 1000000000
        return f"*Account:*\n{public_key}\n*Private key:*\n{private_key}\n*Balance:* {balance}"

    @form_string.register(Wallets)
    async def _(self, wallets: Wallets) -> str:
        returned_string = ""
        for i in wallets:
            returned_string += await self.form_string(i)
            returned_string += "\n-------------\n"
        return returned_string
