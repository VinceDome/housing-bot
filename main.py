import discord, difflib, textwrap
from discord.ext import commands, tasks

from tokens.discordToken import *
from scraper import *

dev_id = 810910872792596550
bot_id = 826458615027597343

client = commands.Bot(command_prefix=".", case_insensitive = True, intents=discord.Intents.all())
client.remove_command("help")

def Diff(platform):
    with open(f"data/diffs/{platform}/old.txt", "r", encoding="utf-8") as f:
        old_page = f.read().strip()

    with open(f"data/diffs/{platform}/new.txt", "r", encoding="utf-8") as f:
        new_page = f.read().strip()


    d = difflib.ndiff(textwrap.wrap(old_page), textwrap.wrap(new_page))

    
    final = ""
    for a in d:
        if not a.startswith("   ") and not a.startswith("  ") and not a.startswith(" ") and a != "\n" and a != "":
            final+=("\n"+a)

    return "```"+final+"```"

@client.event
async def on_ready():  
    print(f'{client.user} active!')
    refresher.start()
    

@client.command()
async def diff(ctx, platform):
    if ctx.author.id != dev_id:
        return None
    
    final = Diff(platform)

    await ctx.send(final)



@tasks.loop(minutes=5)
async def refresher():
    
    result = WholePageUpdate()
    if result != []:
        userD = await client.fetch_user(dev_id)
        msg_dm = await userD.create_dm()
        
        await msg_dm.send(f"{result} had an update!")

        for i in result:
            await msg_dm.send(Diff(i))
        





client.run(MENZA_TOKEN)