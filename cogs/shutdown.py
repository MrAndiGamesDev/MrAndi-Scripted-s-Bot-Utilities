import discord
from discord.ext import commands

class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()  # Only allow bot owner to use this command
    async def shutdown(self, ctx):
        ShutdownEmbed = discord.Embed(
            title="Shuting",
            description="The Bot Down",
            color=discord.Color.blue()
        )
        await ctx.send(embed=ShutdownEmbed)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Shutdown(bot))