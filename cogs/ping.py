from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):  # Changed command name to ping which is more conventional
        await ctx.send(f'🏓 Pong! Latency is {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))