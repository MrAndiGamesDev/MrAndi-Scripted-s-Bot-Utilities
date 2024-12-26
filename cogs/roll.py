import discord
from discord.ext import commands
import random

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, sides: int):
        """Rolls a dice with a specified number of sides."""
        if sides < 1:
            await ctx.send("Please provide a number greater than 0.")
            return
        result = random.randint(1, sides)
        await ctx.send(f"{ctx.author.mention} rolled a {result} on a {sides}-sided dice!")

async def setup(bot):
    await bot.add_cog(Roll(bot))