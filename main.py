import discord
from discord.ext import commands, tasks

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
    CreateFileStructure()
    

@client.command()
async def diff(ctx, platform):
    if ctx.author.id != dev_id:
        return None
    
    final = Diff(platform)

    await ctx.send(final)



@tasks.loop(seconds=30)
async def refresher(): 
    result = WholePageUpdate()
    if result != []:
        userD = await client.fetch_user(dev_id)
        msg_dm = await userD.create_dm()

        await msg_dm.send(f"{result} had an update!")

        for i in result:
            if i == "roomplaza":
                SendMail("Roomplaza update:)", Diff(i))

            try:
                await msg_dm.send(Diff(i))
            except:
                await msg_dm.send("Difference too long")

client.run(MENZA_TOKEN)