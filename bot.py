# bot.py
import os
import discord
import re

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
DICE_ROLLER = os.getenv('DICE_ROLER_NAME')

client = discord.Client()
_next_dc = 10


def parse_dc_value(message):
    try:
        found = re.search(r'[0-9]+', message.content.lower).group(0)
        print(f'{found} FOUND DC')

    except AttributeError:
        found = ''
        print("Not a valid command")

    return found


async def compare(message):
    if not _next_dc:
        await client.send_message(message.channel, "There is no DC or is secret - Ask DM a valid DC")
        return

    dc_value = parse_dc_value(message)

    if dc_value >= _next_dc:
        await client.send_message(message.channel, "Success!")
    else:
        await client.send_message(message.channel, "Failure!")

    return


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author == DICE_ROLLER:
        return compare(message)

    dc_command = '!DC'

    if dc_command in message.content.lower():
        dc_value = parse_dc_value(message)
        if dc_value:
            _next_dc = int(dc_value)


client.run(TOKEN)
