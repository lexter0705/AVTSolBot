import asyncio
from bot.modules.main_database import BotDatabase
from bot.modules.solana_worker import SolanaWorker


class TokenBuyer:
    def __init__(self, solana_worker: SolanaWorker, database: BotDatabase):
        self.__solana_worker = solana_worker
        self.__database = database
        self.__user_in_loop: dict[int, bool] = {}

    async def start_buy_loop(self, user_id: int):
        sender = self.__solana_worker.get_user_sender(user_id)
        self.__user_in_loop[user_id] = True
        while self.__user_in_loop[user_id]:
            user_sleep = self.__database.user_worker.get_user(user_id)[2]
            await asyncio.sleep(user_sleep * 60)
            try:
                await sender.buy_token_on_wallets()
            except Exception as e:
                print(e)
        self.__user_in_loop.pop(user_id)

    async def stop_loop(self, user_id: int):
        self.__user_in_loop[user_id] = False

    def is_in_loop(self, user_id: int) -> bool:
        if user_id in self.__user_in_loop.keys():
            return self.__user_in_loop[user_id]
        return False