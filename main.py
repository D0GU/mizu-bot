
from hashlib import new
import re
import discord
import os
import json
from dotenv import load_dotenv, set_key, find_dotenv

from PIL import Image

from discord.ext import commands


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


bot = commands.Bot(command_prefix=COMMAND_PREFIX)

if not os.path.isdir("reference_images"):
    os.mkdir("reference_images")
    print("reference_images directory created!")
else:
    print("reference_images directory exists!")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello {member.name}~, thanks for coming around cutie~'
    )


@bot.command(name='change.prefix')
async def newprefix(ctx, new_prefix): #Changes the command prefix
    COMMAND_PREFIX = new_prefix
    set_key(dotenv_file, "COMMAND_PREFIX", new_prefix)
    


@bot.command(name='ily')
async def i_love_you(ctx): #Tells the message author that they are loved

    # Takes the username minus id number of the message author
    author = str(ctx.message.author.display_name).split("#")[0] 
    
    response = f"Mmm~ I love you too {author}"
    await ctx.send(response)

@bot.command(name = 'mbuild')
async def build_message_list(ctx):
    text_channels = []
    guild = ctx.message.guild

    try:
        with open(f"{str(guild.id)}msg_history.json", "r") as json_file:
            message_history = json.load(json_file)
    except:
        message_history = {}

    await ctx.send(
        "(re)Building Message database...\n"
        "May take a few minutes depending on message count..."
        )

    for channel in guild.text_channels:
        text_channels.append(channel)

    for channel in text_channels:
        async for msg in channel.history(limit=10000):
            if msg.id not in message_history:
                message_history[msg.id] = {'user': str(msg.author.name), 'content': str(msg.content)}
                print(f'{str(msg.author.name)} : {str(msg.content)}')
            else:
             return
        
    with open(f"{str(guild.id)}_msg_history.json", "w") as json_data:
            json_data.write(json.dumps(message_history))
    
    await ctx.send(f"<@{str(ctx.message.author.id)}>, Message Database Built!")
        
@bot.command(name="wordusage") 
async def wordusage(ctx, word: str): # Checks how many times a word is used within the user's guild.
    count = 0
    guild = ctx.message.guild
    print(f"current guild id is: {guild.id}")
    try:
        with open(f"{str(guild.id)}_msg_history.json", "r") as json_file:
            message_history = json.load(json_file)
    except:
        await ctx.send(
            "Could not find message database\n"
            f"Please type '{commandprefix}mbuild' to build message database"
        )
        
    for msg in message_history:
        if word.lower() in message_history[msg]['content'].lower():
            print(message_history[msg]["content"])
            count += 1
    await ctx.send(f"The word {word} has been used {count} times on this server")


@bot.command(name = "create")
async def create_entry(ctx, name):
    references = {}
    try:
        with open("references.json", "r") as json_data:
                references = json.load(json_data)
    except:
        await ctx.send("reference file could not be opened, contact D0GU#5777")

    if name in references:
        await ctx.send("Name already in references")
    else:
        references[name] = {
            "age": 0,
            "height": 0,
            "description": ""
        }
        with open("references.json", "w") as fileout:
            fileout.write(json.dumps(references))
        await ctx.send(f"Reference for character {name} has been created")


@bot.command(name = "update")
async def create_entry(ctx, name, parameter: str, content):
    references = {}
    try:
        with open("references.json", "r") as json_data:
                references = json.load(json_data)
    except:
        await ctx.send("reference file could not be opened, contact D0GU#5777")
    
    if parameter == "age":
        references[name]["age"] = content
    elif parameter == "height":
        references[name]["height"] = content
    elif parameter == "description":
        references[name]["description"] = content

    with open("references.json", "w") as json_data:
        json_data.write(json.dumps(references))

    await ctx.send(f"{name}'s {parameter} has been updated")

@bot.command(name = "update.image")
async def create_entry(ctx, name):
    references = {}
    try:
        with open("references.json", "r") as json_data:
                references = json.load(json_data)
    except:
        await ctx.send("reference file could not be opened, contact D0GU#5777")

    if name in references:
        for attach in ctx.message.attachments:
            await attach.save(f"reference_images/{attach.filename}")
            im = Image.open(f"reference_images/{attach.filename}")
            im.save(f"reference_images/{name}.png") 
            os.remove(f"reference_images/{attach.filename}")
            
    await ctx.send(f"{name}'s reference image updated")


@bot.command(name = "reference")
async def reference(ctx, name):
    references = {}
    try:
        with open("references.json", "r") as json_data:
                references = json.load(json_data)
    except:
        await ctx.send("reference file could not be opened, contact D0GU#5777")

    age = (str(references[name]['age']))
    height = (str(references[name]['height']))
    desc = references[name]['description']

    if name in references:
        file = discord.File(f"reference_images/{name}.png")
        embed = discord.Embed(title=name, description="Character Reference", color=0x73d216)
        embed.add_field(name="Age", value=age, inline=True)
        embed.add_field(name="Height", value=(height+"cm"), inline=True)
        embed.add_field(name="Description", value=desc, inline=False)
        embed.set_image(url=f"attachment://reference_images/{name}.png")
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send("Character not in references")

bot.run(TOKEN)