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

    if message.content.startswith('$j'):
        await message.channel.send(brain.gen_text())

client.run(settings['token'])
