import os
import time
import discord
from discord.ext import commands
from mcrcon import MCRcon, MCRconException
from dotenv import load_dotenv
import asyncio

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
RCON_HOST = os.getenv('RCON_HOST')
RCON_PORT = int(os.getenv('RCON_PORT'))
RCON_PASSWORD = os.getenv('RCON_PASSWORD')
MC_LOG_FILE = os.getenv('MC_LOG_FILE')

print(f'DISCORD_TOKEN: {DISCORD_TOKEN}')
print(f'DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}')
print(f'RCON_HOST: {RCON_HOST}')
print(f'RCON_PORT: {RCON_PORT}')
print(f'RCON_PASSWORD: {RCON_PASSWORD}')
print(f'MC_LOG_FILE: {MC_LOG_FILE}')

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

    while not bot.is_closed():
        try:
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                response = mcr.command('custom_log_fetch_command')  # Replace with actual command if available
                if response:
                    await channel.send(response)
        except MCRconException as e:
            print(f"Failed to fetch logs: {str(e)}")
        await asyncio.sleep(10)

@bot.command(name='send')
async def send_to_minecraft(ctx, *, message):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(f'say {message}')
            await ctx.send(f'Message sent to Minecraft: {message}')
    except Exception as e:
        await ctx.send(f'Failed to send message: {str(e)}')

@bot.command(name='on')
async def online_players(ctx):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command('list')
            await ctx.send(f'Online players: {response}')
    except Exception as e:
        await ctx.send(f'Failed to check online players: {str(e)}')

bot.run(DISCORD_TOKEN)
