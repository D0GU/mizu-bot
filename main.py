from email import message
from enum import auto
from tokenize import String
import discord
import os
import json
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix=">")




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
    author = str(ctx.message.author).split("#")[0] 
    
    response = f"Mmm~ I love you too {author}~"
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
            

bot.run(TOKEN)