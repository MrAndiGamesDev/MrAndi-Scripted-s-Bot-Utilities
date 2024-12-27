import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, ctx):
        """Generates and sends an invite link to the server."""
        try:
            # Check if the bot has permission to create invites
            if not ctx.guild.me.guild_permissions.create_instant_invite:
                return await ctx.send("I don't have permission to create an invite link. Please check my permissions.")

            # Check if the user has permission to generate an invite
            if not ctx.author.guild_permissions.manage_guild:
                return await ctx.send("You do not have permission to generate an invite link.")

            # Create a server invite with no expiration and unlimited uses
            invite = await ctx.channel.create_invite(
                max_age=0, max_uses=0  # Never expire, infinite uses
            )
            await ctx.send(f"Here is your invite link to join the server: {invite.url}")

        except discord.Forbidden:
            await ctx.send("I don't have permission to create an invite link. Please check my permissions.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while creating the invite link: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Invite(bot))