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

help_mesg = "```{0}j - Prints out a statement\n{0}help - Prints out help statement ```"
bot_description = settings['bot_description']

bot = commands.Bot(command_prefix=settings['commandKey'], description=bot_description)
brain = MarkovBrain().load(settings['MarkovChain'])

@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user.name))
    print('-------')

@bot.command(description='Prints generated text')
async def J(ctx):
    mesg = brain.gen_text()
    while(mesg == ""):
        mesg = brain.gen_text()
    logger.info("{}: {}".format(ctx.author, mesg))
    print("{}: {}".format(ctx.author, mesg))
    await ctx.send(mesg)


bot.run(settings['token'])
