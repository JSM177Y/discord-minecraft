import os
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
MC_LOG_FILE = os.getenv('MC_LOG_FILE')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected to Discord!')
    bot.loop.create_task(monitor_minecraft_log())

async def monitor_minecraft_log():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))

    with open(MC_LOG_FILE, 'r') as log_file:
        log_file.seek(0, os.SEEK_END)  # Move to the end of the file

        while not bot.is_closed():
            line = log_file.readline()
            if line:
                await channel.send(line.strip())
            await asyncio.sleep(1)

@bot.command(name='send')
async def send_to_minecraft(ctx, *, message):
    try:
        # You can implement sending message to Minecraft via RCON here
        await ctx.send(f'Message sent to Minecraft: {message}')
    except Exception as e:
        await ctx.send(f'Failed to send message: {str(e)}')

@bot.command(name='on')
async def online_players(ctx):
    try:
        # You can implement fetching online players via RCON here
        await ctx.send(f'Online players: ...')
    except Exception as e:
        await ctx.send(f'Failed to check online players: {str(e)}')

bot.run(DISCORD_TOKEN)
