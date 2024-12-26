from discord.ext import commands

class Getbadge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def getbadge(self, ctx):
        """Provides information about getting the Active Developer Badge"""
        await ctx.send("To get the Active Developer Badge, follow this link:\nhttps://discord.com/developers/active-developer")

async def setup(bot):
    await bot.add_cog(Getbadge(bot))

