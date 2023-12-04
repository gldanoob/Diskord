import asyncio
from pathlib import Path

from backend import bot
from util.file import compress, empty_folder, extract

FILENAME = "horny.jpeg"


async def main():
    target = Path("generated").joinpath(FILENAME).with_suffix(".7z")
    source = Path("data").joinpath(FILENAME)
    output = Path("output")

    await bot.start()
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
