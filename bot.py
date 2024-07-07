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
RCON_PORT = int(os.getenv('RCON_PORT'))
RCON_PASSWORD = os.getenv('RCON_PASSWORD')

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
    try:
        with mcrcon.MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(f'say {message}')
            await ctx.send(f'Message sent to Minecraft: {message}')
    except Exception as e:
        await ctx.send(f'Failed to send message: {str(e)}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Post Discord message to Minecraft server
    try:
        with mcrcon.MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            mcr.command(f'say {message.content}')
    except Exception as e:
        print(f'Failed to send message: {str(e)}')

    await bot.process_commands(message)

bot.run(TOKEN)
