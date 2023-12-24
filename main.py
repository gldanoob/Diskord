import asyncio
import os
from pathlib import Path

import dotenv

from backend import bot
from util.errors import BotError
from util.file import compress, empty_folder, extract

dotenv.load_dotenv()

FILENAME = "horny.jpeg"

TARGET = Path("generated")
SOURCE = Path("data")
OUTPUT = Path("output")

PASSWORD = "gay"


async def store_file(filename: str) -> int:
    file_paths = compress(
        TARGET.joinpath(filename + ".7z"),
        PASSWORD,
        SOURCE.joinpath(filename)
    )

    message_ids = []

    thread_id = await bot.create_thread(filename)
    for file_path in file_paths:
        mid = await bot.send(thread_id, file=file_path)
        message_ids.append(mid)

    return thread_id


async def retrieve_file(filename: str, thread_id: int):
    message_ids = await bot.retrieve_ids(thread_id)
    await bot.download_messages(thread_id, message_ids, TARGET)
    extract(TARGET.joinpath(filename), PASSWORD, OUTPUT)


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise BotError("DISCORD_TOKEN is not set in .env")
    await bot.start(token)

    empty_folder(TARGET)
    empty_folder(OUTPUT)

    # compress and send
    thread_id = await store_file(FILENAME)

    # download and extract
    empty_folder(Path("generated"))

    await retrieve_file(FILENAME, thread_id)


asyncio.run(main())
