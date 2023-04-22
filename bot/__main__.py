# noqa: D100
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFahter
TOKEN = os.getenv("CODEWARS_BOT_TOKEN", "")

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """Receives messages with `/start` command."""
    username = getattr(message.from_user, "full_name", "stranger")
    await message.answer(f"Hello, <b>{username}!</b>")


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Forward received message back to the sender.

    By default, message handler will handle all message types
    (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
