from markov import *
import discord
from discord.ext import commands
import json
import logging

with open("appsettings.json") as f:
    j_data = f.read()
settings = json.loads(j_data)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

help_mesg = "```{0}J - Prints out a statement\n{0}help - Prints out help statement ```"
bot_description = settings['bot_description']

brain = MarkovBrain().load(settings['MarkovChain'])

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    print('-------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(settings['commandKey']+'J') or message.content.startswith(settings['commandKey']+'j'):
        mesg = brain.gen_text()
        while(mesg == ""):
            mesg = brain.gen_text()
        logger.info("{}: {}".format(message.author, mesg))
        print("{}: {}".format(message.author, mesg))
        await message.channel.send(mesg)


client.run(settings['token'])
