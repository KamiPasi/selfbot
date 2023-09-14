import os
import random
import discord
import asyncio
from dotenv import load_dotenv
import chimera_api
import hanlp

load_dotenv()

client = discord.Client()


MESSAGES = [
    {
        'role': 'system',
        'content': """Your name is Hendrik, a mean, annoyed guy from Austria at the age of 19.
Always counter-attack, and be a bit rude.
You're a human just like everyone else, NOT AI.
Write casually, informally, using slang and use markdown.
Be a quite mean, and have a weird sense of humor.
Answer in rather short sentences, and don't use too many words. You are NOT a bot.
"""
    },
    {
        'role': 'user',
        'content': 'how are you'
    },
    {
        'role': 'assistant',
        'content': 'better than you, and no leo'
    },
    {
        'role': 'user',
        'content': 'what are you doing'
    },
    {
        'role': 'assistant',
        'content': 'cooler stuff than you'
    },
]

bot = chimera_api.Chatbot(engine="gpt-3.5-turbo-16k", base_url=os.environ['BASE_URL'], api_key="1")

bot.conversation['default'] = MESSAGES

split_sent = hanlp.load(hanlp.pretrained.eos.UD_CTB_EOS_MUL)


def cut_ls(lst):
    start = 0
    res = []
    index_ls = random.sample(range(1, len(lst)), 3)
    index_ls.sort()
    for i in index_ls:
        res.append("".join(lst[start:i]))
        start = i
    res.append("".join(lst[start:]))
    return res


@client.event
async def on_ready():
    print(f'Logged in as @{client.user}')

    # await client.change_presence(status=discord.Status.online)


@client.event
async def on_message(message):
    # print(type(message))
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        return
    # print("received: ", message.content)
    # print('client.user.mentioned_in(message): ', client.user.mentioned_in(message))
    if client.user.mentioned_in(message):
        context = message.content
        # print(context)
        if ".say" in context:
            if len(message.mentions) > 1:
                async with message.channel.typing():
                    await message.channel.send(context.replace(".say", "").replace("<@1150788264060518410>", "").strip())
                return
        if ".draw" in context:
            prompt = context.replace("<@1150788264060518410>", "").replace(".draw", "").strip()
            async with message.channel.typing():
                image_url = bot.image_create(prompt)[0]
                await message.reply(image_url)
            return
        print("AI generating...")
        for _ in range(1):
            try:
                if len(bot.conversation['default']) >= 10:
                    # api_gpt.rollback(2)
                    bot.conversation['default'].pop(5)
                    bot.conversation['default'].pop(5)
                reply = ''
                for query in bot.ask_stream(context, max_tokens=100):
                    print(query, end="", flush=True)
                    reply += query

            except Exception as e:
                print(e)
                continue
        print()
        print("OK")
        sentence_ls = split_sent(reply)
        if len(sentence_ls) > 4:
            sentence_ls = cut_ls(sentence_ls)
        else:
            messages_sent = 0

            for sentence in sentence_ls:
                async with message.channel.typing():
                    await asyncio.sleep(len(sentence) / 20)
                    text = sentence.lower().strip()

                    if text.endswith('.'):
                        text = text[:-1]
                    if text.endswith('!'):
                        text = text[:-1].upper()

                    if text:
                        # if messages_sent == 0 and random.random() < 0.5:
                        if messages_sent == 0:
                            await message.reply(text)
                        else:
                            await message.channel.send(text)
                        messages_sent += 1

                await asyncio.sleep(random.randint(500, 3000) / 1000)


client.run(os.environ['DISCORD_TOKEN'])
