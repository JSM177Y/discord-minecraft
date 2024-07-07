import discord
from discord.ext import commands
from mcstatus import MinecraftServer

bot = commands.Bot(command_prefix="!")
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
MINECRAFT_SERVER_IP = 'YOUR_MINECRAFT_SERVER_IP'

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is connected to Discord!')

@bot.command(name='send')
async def send_to_minecraft(ctx, *, message):
    # Send message to Minecraft server (requires Crafty API or RCON setup)
    # Example using RCON:
    server = MinecraftServer.lookup(MINECRAFT_SERVER_IP)
    status = server.status()
    await ctx.send(f'Online players: {status.players.online}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Post Discord message to Minecraft server
    # This requires Crafty API or RCON setup
    # Example code here

    await bot.process_commands(message)

bot.run(TOKEN)
