from markov import *
import discord
import json

with open("appsettings.json") as f:
    j_data = f.read()
settings = json.loads(j_data)
client = discord.Client()
brain = MarkovBrain().load(settings['MarkovChain'])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(settings['commandKey']):
        quote = brain.gen_text()
        while(quote == ""):
            quote = brain.gen_text()
        await message.channel.send(quote)

client.run(settings['token'])
