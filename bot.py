import os
import time
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from icecream import ic

load_dotenv()

TOKEN = os.getenv("TOKEN")
MSG_DID = "Are you {} did your homework today?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f"{user_id=} - {user_full_name=}: {time.asctime()}")

    await message.reply(f"Hello, {user_full_name}!")

    for i in range(7):
        time.sleep(360*24)
        ic(MSG_DID.format(user_name), user_name)
        logging.info(f"{user_name}")
        logging.info(f"{user_id=} - {user_name=}: {MSG_DID.format(user_name)}")
        await bot.send_message(user_id, MSG_DID.format(user_name))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiogram.contrib.fsm_storage").setLevel(logging.WARNING)
    logging.getLogger("aiogram.contrib.middlewares").setLevel(logging.WARNING)
    logging.getLogger("aiogram.dispatcher.filters").setLevel(logging.WARNING)

    executor.start_polling(dp)
