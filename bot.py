import discord
from discord.ext import commands
import mcrcon
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RCON_IP = os.getenv('RCON_IP')
RCON_PORT = os.getenv('RCON_PORT')
RCON_PASSWORD = os.getenv('RCON_PASSWORD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Add the channel ID to your .env file

# Debugging prints
print(f'DISCORD_BOT_TOKEN: {TOKEN}')
print(f'RCON_IP: {RCON_IP}')
print(f'RCON_PORT: {RCON_PORT}')
print(f'RCON_PASSWORD: {RCON_PASSWORD}')
print(f'CHANNEL_ID: {CHANNEL_ID}')

# Convert RCON_PORT to integer if it's not None
if RCON_PORT:
    RCON_PORT = int(RCON_PORT)

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected to Discord!')

@bot.command(name='send')
async def send_to_minecraft(ctx, *, message):
    if ctx.channel.id != CHANNEL_ID:
        return  # Ignore if not in the specified channel

    try:
        with mcrcon.MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(f'say {message}')
            await ctx.send(f'Message sent to Minecraft: {message}')
    except Exception as e:
        await ctx.send(f'Failed to send message: {str(e)}')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != CHANNEL_ID:
        return  # Ignore messages from the bot itself or not from the specified channel

    # Post Discord message to Minecraft server
    try:
        with mcrcon.MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            mcr.command(f'say {message.content}')
    except Exception as e:
        print(f'Failed to send message: {str(e)}')

    await bot.process_commands(message)

bot.run(TOKEN)
