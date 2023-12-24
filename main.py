import asyncio
import os
from pathlib import Path

import dotenv

from backend import bot
from backend.api import API, start_server
from util.errors import BotError
from util.file import compress, empty_folder, extract
from util.logging import log

dotenv.load_dotenv()

FILENAME = "horny.jpeg"

TARGET = Path("generated")
SOURCE = Path("data")
OUTPUT = Path("output")

PASSWORD = "gay"


@API("/store")
async def store_file(filename: str = "") -> int:
    if filename == "":
        raise BotError("EMPTY FILENAME")

    if not SOURCE.joinpath(filename).exists():
        raise BotError("FILE NOT FOUND")

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


@API("/retrieve")
async def retrieve_file(filename: str = "", thread_id: str = ""):
    if filename == "":
        raise BotError("EMPTY FILENAME")

    if thread_id == "":
        raise BotError("EMPTY THREAD ID")

    thread_id_int = int(thread_id)
    message_ids = await bot.retrieve_ids(int(thread_id_int))
    await bot.download_messages(thread_id_int, message_ids, TARGET)
    extract(TARGET.joinpath(filename), PASSWORD, OUTPUT)


async def main():
    try:
        token = os.getenv("DISCORD_TOKEN")
        if token is None:
            raise BotError("DISCORD_TOKEN is not set in .env")
        await bot.start(token)

        await start_server()

        empty_folder(TARGET)
        empty_folder(OUTPUT)

        while True:
            await asyncio.sleep(3600)

    except (KeyboardInterrupt, asyncio.CancelledError) as e:
        log("Exiting...")


asyncio.run(main())
