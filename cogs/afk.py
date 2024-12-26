import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        """Sets your AFK status."""
        self.afk_users[ctx.author.id] = reason
        await ctx.send(f"{ctx.author.mention} is now AFK: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            await message.channel.send(f"Welcome back, {message.author.mention}! I have removed your AFK status.")
        
        for user_id, reason in self.afk_users.items():
            if message.guild and message.guild.get_member(user_id):
                user = message.guild.get_member(user_id)
                if user in message.mentions:
                    await message.channel.send(f"{user.mention} is currently AFK: {reason}")

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(AFK(bot))