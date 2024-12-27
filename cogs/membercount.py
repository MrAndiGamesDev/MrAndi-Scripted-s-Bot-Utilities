import discord
from discord.ext import commands

class MemberCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def membercount(self, ctx):
        """Displays the number of members in the server."""
        member_count = ctx.guild.member_count
        MemberCountEmbed = discord.Embed(
            title="Total Number Of Members",
            description=f"in this server is: {member_count}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=MemberCountEmbed)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(MemberCount(bot))