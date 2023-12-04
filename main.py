import asyncio
import os
from pathlib import Path

import dotenv

from backend import bot
from util.errors import BotError
from util.file import compress, empty_folder, extract

dotenv.load_dotenv()

FILENAME = "horny.jpeg"


async def main():
    target = Path("generated").joinpath(FILENAME).with_suffix(".7z")
    source = Path("data").joinpath(FILENAME)
    output = Path("output")

    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise BotError("DISCORD_TOKEN is not set in .env")
    await bot.start(token)
    await bot.send("my waif")

    message_ids = []

    empty_folder(Path("generated"))
    empty_folder(Path("output"))

    # compress and send
    files = compress(target, "moan", source)

    for f in files:
        mid = await bot.send(file=Path(f))
        message_ids.append(mid)

    # download and extract
    empty_folder(Path("generated"))
    await bot.download_messages(message_ids, Path("generated"))
    extract(target, "moan", output)


asyncio.run(main())
