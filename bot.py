# bot.py
import os
import discord
import re

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
DICE_ROLLER = os.getenv('DICE_ROLER_NAME')

client = discord.Client()
_dcs = {}
_dc_command = '!dc'


def parse_dc_value(message):
    try:
        found = int(re.search(r'[0-9]+', message.content.lower()).group(0))
    except AttributeError:
        found = ''
        print("Not a valid command")

    return found


async def compare(message):
    print(f'{_dcs} NEXT DC!')

    if not _dcs:
        await client.send_message(message.channel, "There is no DC or is secret - Ask DM a valid DC")
        return

    dc_value = parse_dc_value(message)

    print(f'{dc_value} VALUE ROLLED!')

    if dc_value >= _dcs[message.guild.id]:
        await message.channel.send("Success!")
    else:
        await message.channel.send("Failure!")

    return


async def set_dc(message):

    if message.content.lower().startswith(_dc_command):
        dc_value = parse_dc_value(message)
        if dc_value:
            _dcs[message.guild.id] = int(dc_value)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{DICE_ROLLER} depending on ')


@client.event
async def on_message(message):
    author = str(message.author).strip()
    if author == client.user:
        return

    print(f'{author} Message Author')
    print(f'{message.guild.id} GuildId')

    if author == DICE_ROLLER:
        return await compare(message)

    await set_dc(message)


client.run(TOKEN)
