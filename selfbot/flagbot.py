import os
import json
import discord

from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as @{client.user}')
    await client.change_presence(status=discord.Status.online)

countries = json.load(open('countries.json'))

@client.event
async def on_message(message):
    if message.channel.id == 1122625339697397852 and message.author.name == 'kamipasi':
        tld = message.embeds[0].to_dict()['image']['url'].split('/')[-1].split('.')[0]
        await message.channel.send(countries[tld])

client.run(os.environ['DISCORD_TOKEN'])
