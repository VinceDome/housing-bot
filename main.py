import os, discord, time, random, asyncio, math
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord.ui import Button, View

from tokens.discordToken import *
from scraper import *

dev_id = 810910872792596550
bot_id = 826458615027597343

client = commands.Bot(command_prefix=".", case_insensitive = True, intents=discord.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():  
    print(f'{client.user} active!')
    refresher.start()
    

@client.command()
async def sync(ctx):
    if ctx.author.id != dev_id:
        return None
    
    await ctx.send("lol")



@tasks.loop(minutes=5)
async def refresher():
    
    result = pageUpdate()
    if result is not None:
        userD = await client.fetch_user(dev_id)
        msg_dm = await userD.create_dm()
        await msg_dm.send(f"[{result}] had an update!")






client.run(MENZA_TOKEN)