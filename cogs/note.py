import discord
from discord.ext import commands

class NoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = {}

    @commands.command()
    async def note(self, ctx, *, content: str):
        """Adds a personal note."""
        if ctx.author.id not in self.notes:
            self.notes[ctx.author.id] = []
        self.notes[ctx.author.id].append(content)
        await ctx.send(f"Note added: {content}")

    @commands.command()
    async def notes(self, ctx):
        """Displays your personal notes."""
        if ctx.author.id not in self.notes or not self.notes[ctx.author.id]:
            await ctx.send("You have no notes.")
        else:
            user_notes = self.notes[ctx.author.id]
            notes_message = "\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(user_notes))
            await ctx.send(f"Your notes:\n{notes_message}")

    @commands.command()
    async def clearnotes(self, ctx):
        """Clears all your personal notes."""
        self.notes[ctx.author.id] = []
        await ctx.send("All your notes have been cleared.")

def setup(bot):
    bot.add_cog(NoteCog(bot))