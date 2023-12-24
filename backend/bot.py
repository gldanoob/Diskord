import asyncio
import functools
import typing
from pathlib import Path

import discord

from util.errors import BotError
from util.logging import log

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

is_ready = asyncio.Event()

STORAGE_CHANNEL = 1180990620798554215


@client.event
async def on_ready():
    log("BOT READY")
    is_ready.set()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Create a thread in the storage channel with given name


async def create_thread(name: str) -> int:
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    if name == "":
        raise BotError("EMPTY THREAD NAME")

    channel = client.get_channel(STORAGE_CHANNEL)
    if not isinstance(channel, discord.ForumChannel):
        raise BotError("CHANNEL NOT A FORUM")

    log(f"Creating thread: {name}")
    thread = await channel.create_thread(name=name, content="WAKE TF UP")
    return thread.thread.id


async def send(thread_id: int, message: str | None = None, file: Path | None = None) -> int:
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    thread = client.get_channel(thread_id)
    if not isinstance(thread, discord.Thread):
        raise BotError("CHANNEL NOT A THREAD")

    if file is not None:
        log(f"Sending file: {file}")
        discord_message = await thread.send(file=discord.File(file), content=message)
        return discord_message.id
    elif message is not None:
        log(f"Sending message: {message}")
        discord_message = await thread.send(message)
        return discord_message.id
    else:
        raise BotError("NO MESSAGE OR FILE")


# Retreive all message ids with an attachments from a thread
async def retrieve_ids(thread_id: int) -> list[int]:
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    thread = client.get_channel(thread_id)
    if not isinstance(thread, discord.Thread):
        raise BotError("CHANNEL NOT A THREAD")

    return [m.id async for m in thread.history() if len(m.attachments) == 1]


async def download_messages(thread_id: int, message_ids: list[int], output: Path):
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    thread = client.get_channel(thread_id)
    if not isinstance(thread, discord.Thread):
        raise BotError("CHANNEL NOT A THREAD")

    for mid in message_ids:
        message = await thread.fetch_message(mid)
        if len(message.attachments) == 0:
            raise BotError("MESSAGE HAS NO ATTACHMENTS")

        log(f"Downloading file: {message.attachments[0].filename}")
        await message.attachments[0].save(output.joinpath(message.attachments[0].filename))


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


async def start(token: str):
    asyncio.create_task(client.start(token))
    log("Waiting for bot to be ready...")
    await is_ready.wait()
