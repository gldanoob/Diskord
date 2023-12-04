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


async def send(message: str | None = None, file: Path | None = None):
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    channel = client.get_channel(1180990853485965475)
    if not isinstance(channel, discord.Thread):
        raise BotError("CHANNEL NOT A THREAD")

    if file is not None:
        log(f"Sending file: {file}")
        discord_message = await channel.send(file=discord.File(file), content=message)
        return discord_message.id
    elif message is not None:
        log(f"Sending message: {message}")
        discord_message = await channel.send(message)
        return discord_message.id


async def download_messages(message_ids: list[int], output: Path):
    if not client.is_ready():
        raise BotError("BOT NOT READY")

    channel = client.get_channel(1180990853485965475)
    if not isinstance(channel, discord.Thread):
        raise BotError("CHANNEL NOT A THREAD")

    for mid in message_ids:
        message = await channel.fetch_message(mid)
        if len(message.attachments) == 0:
            raise BotError("MESSAGE HAS NO ATTACHMENTS")

        log(f"Downloading file: {message.attachments[0].filename}")
        await message.attachments[0].save(output.joinpath(message.attachments[0].filename))


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


async def start():
    asyncio.create_task(client.start(
        'MTE4MTAxOTE3Mjk1MjYwODgxOA.Ga51RM.vGgx_Ij_fndbEjGKW_ur3DIdgHJZV6om4z4f9E'))
    log("Waiting for bot to be ready...")
    await is_ready.wait()
