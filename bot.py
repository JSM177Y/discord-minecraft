import discord
from discord.ext import commands, tasks
import mcrcon
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Get environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RCON_IP = os.getenv('RCON_IP', 'localhost')
RCON_PORT = int(os.getenv('RCON_PORT', 25575))
RCON_PASSWORD = os.getenv('RCON_PASSWORD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected to Discord!')
    monitor_minecraft_chat.start()  # Start the background task

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
        print(f'Error details: {e}')  # Additional debug information

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

@tasks.loop(seconds=5)  # Run this task every 5 seconds
async def monitor_minecraft_chat():
    try:
        with mcrcon.MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command("list")  # Example command to keep connection alive
            # Add code here to fetch and handle chat messages
            # This depends on your Minecraft server setup and available RCON commands
            # For now, we will simulate with an example message
            # Replace this with actual fetching of chat logs from your server
            example_message = "Player1: Hello from Minecraft!"
            
            # Check if this is a new message and send it to Discord
            # For simplicity, let's just send the example message
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(example_message)
            
            time.sleep(5)  # Sleep to simulate waiting for new messages
    except Exception as e:
        print(f'Failed to monitor Minecraft chat: {str(e)}')

bot.run(TOKEN)
