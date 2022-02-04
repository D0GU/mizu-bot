from email import message
from enum import auto
from tokenize import String
from unicodedata import name
import discord
import os
import json
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

commandprefix = ">"
bot = commands.Bot(command_prefix=commandprefix)




@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello {member.name}~, thanks for coming around cutie~'
    )

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
        return
    for msg in message_history:
        if word.lower() in message_history[msg]['content'].lower():
            print(message_history[msg]["content"])
            count += 1
    await ctx.send(f"The word {word} has been used {count} times on this server")


@bot.command(name = "create_entry")
async def create_entry(ctx, name):
    try:
        with open("references.json", "r") as json_data:
            references =  json_data.load(json_data)
    except:
        await ctx.send("Could not open references")
        return

    if name in references:
        await ctx.send("Name already in references")
    else:
        references[name] = {
            "age": 0,
            "height": 0,
            "description": ""
        }
        with open("references,json", "r") as fileout:
            fileout.write(json.dumps(references))
        await ctx.send(f"Reference for character {name} has been created")


bot.run(TOKEN)