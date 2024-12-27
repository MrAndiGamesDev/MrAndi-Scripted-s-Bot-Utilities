import discord
from discord.ext import commands
import os
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

# Load config
with open('config.json') as f:
    config = json.load(f)

# Bot setup with intents
intents = discord.Intents.default()  # Using default intents is safer
intents.message_content = True  # Enable message content intent specifically
intents.typing = True
bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)

token = os.getenv("TOKEN")

async def send_status_message(status: str, color: discord.Color):
    channel = bot.get_channel(config['StatusChannelID'])
    if channel:
        embed = discord.Embed(
            title="Bot Status Update",
            description=status,
            color=color,
            timestamp=datetime.datetime.now()
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

    async def animated_pfp(bot, gif_path):
        """Updates the bot's profile picture to an animated GIF."""
        try:
            # Check if the provided GIF path exists
            if not os.path.exists(gif_path):
                print(f"Error: The GIF file at {gif_path} was not found.")
                return

            # Open and read the GIF file
            with open(gif_path, 'rb') as gif_file:
                gif_data = gif_file.read()

            # Update the bot's profile picture
            await bot.user.edit(avatar=gif_data)
            print("Bot profile picture updated to a GIF.")

        except Exception as e:
            # Catch and log any exceptions that occur
            print(f"An error occurred while updating the bot's profile picture: {e}")

    async def load_extensions_from_directory(directory: str, extension_type: str) -> None:
        try:
            for filename in os.listdir(f'./{directory}'):
                if filename.endswith('.py'):
                    extension_name = f'{directory}.{filename[:-3]}'
                    await bot.load_extension(extension_name)
                    print(f'Loaded {extension_type}: {filename[:-3]}')
        except Exception as e:
            print(f'Error loading {extension_type}s: {e}')
            await send_status_message(f"Error loading {extension_type}s: {e} ⚠️", discord.Color.orange())

    await animated_pfp(bot, "./tenor.gif")
    await load_extensions_from_directory('cogs', 'cog')

@bot.event
async def on_disconnect():
    await send_status_message("Bot has disconnected! 🔴", discord.Color.red())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use !help to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required argument! Please check command usage with !help.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided! Please check command usage with !help.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Unhandled error: {error}")

# Run the bot
if not token:
    raise ValueError("No token found in .env file")
    
try:
    bot.run(token)
except discord.LoginFailure:
    print("Failed to login: Invalid token")
except Exception as e:
    print(f'Error running bot: {e}')