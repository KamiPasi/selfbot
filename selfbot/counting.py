import os
import discord

from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as @{client.user}')
    await client.change_presence(status=discord.Status.online)

@client.event
async def on_message(message):
    if message.channel.id == 1118997624100499550:
        i = int(message.content)
        await message.channel.send(i - 1)

client.run(os.environ['DISCORD_TOKEN'])
