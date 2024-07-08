import os
import time
import discord
from discord.ext import commands
from mcrcon import MCRcon
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
RCON_HOST = os.getenv('RCON_HOST')
RCON_PORT = os.getenv('RCON_PORT')
RCON_PASSWORD = os.getenv('RCON_PASSWORD')

print(f'DISCORD_TOKEN: {DISCORD_TOKEN}')
print(f'DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}')
print(f'RCON_HOST: {RCON_HOST}')
print(f'RCON_PORT: {RCON_PORT}')
print(f'RCON_PASSWORD: {RCON_PASSWORD}')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected to Discord!')
    bot.loop.create_task(monitor_minecraft_chat())

async def monitor_minecraft_chat():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))

    with MCRcon(RCON_HOST, RCON_PASSWORD, port=int(RCON_PORT)) as mcr:
        last_log = ""

        while not bot.is_closed():
            # Assuming you have a way to fetch the latest chat message
            response = mcr.command('latest_chat_message')  # Replace with actual command to get the latest chat message
            print(f"Received response from server: {response}")
            if response != last_log:
                await channel.send(response)
                last_log = response
            time.sleep(5)

@bot.command(name='send')
async def send_to_minecraft(ctx, *, message):
    try:
        print(f"Sending message to Minecraft: {message}")
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=int(RCON_PORT)) as mcr:
            response = mcr.command(f'say {message}')
            print(f"Received response from server after sending message: {response}")
            await ctx.send(f'Message sent to Minecraft: {message}')
    except Exception as e:
        print(f"Failed to send message: {str(e)}")
        await ctx.send(f'Failed to send message: {str(e)}')

@bot.command(name='on')
async def online_players(ctx):
    try:
        print(f"Checking online players")
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=int(RCON_PORT)) as mcr:
            response = mcr.command('list')
            print(f"Received response from server: {response}")
            await ctx.send(f'Online players: {response}')
    except Exception as e:
        print(f"Failed to check online players: {str(e)}")
        await ctx.send(f'Failed to check online players: {str(e)}')

bot.run(DISCORD_TOKEN)
