import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()

# Load config
with open('config.json') as f:
    config = json.load(f)

# Bot setup with intents
intents = discord.Intents.default()  # Using default intents is safer
intents.message_content = True  # Enable message content intent specifically
bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="!help | Bot is ready!"))

async def send_status_message(status: str, color: discord.Color):
    """Send bot status message to status channel"""
    channel = bot.get_channel(config['StatusChannelID'])
    if channel:
        embed = discord.Embed(
            title="Bot Status Update",
            description=status,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )
        await channel.send(embed=embed)

# Cog loading
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await send_status_message("Bot is now online! 🟢", discord.Color.green())
    
    # Set custom status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Use | !help"
        ),
        status=discord.Status.online
    )

    async def load_extensions_from_directory(directory: str, extension_type: str) -> None:
        """Load all Python files as extensions from the specified directory."""
        try:
            for filename in os.listdir(f'./{directory}'):
                if filename.endswith('.py'):
                    extension_name = f'{directory}.{filename[:-3]}'
                    await bot.load_extension(extension_name)
                    print(f'Loaded {extension_type}: {filename[:-3]}')
        except Exception as e:
            print(f'Error loading {extension_type}s: {e}')
            await send_status_message(f"Error loading {extension_type}s: {e} ⚠️", discord.Color.orange())

    await load_extensions_from_directory('cogs', 'cog')

@bot.event
async def on_disconnect():
    await send_status_message("Bot has disconnected! 🔴", discord.Color.red())

# Run the bot
token = os.getenv("TOKEN")
if not token:
    raise ValueError("No token found in .env file")
    
try:
    bot.run(token)
except discord.LoginFailure:
    print("Failed to login: Invalid token")
except Exception as e:
    print(f'Error running bot: {e}')