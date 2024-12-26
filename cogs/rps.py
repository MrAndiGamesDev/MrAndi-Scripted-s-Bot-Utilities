from discord.ext import commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, choice: str):
        """Play a game of rock-paper-scissors. Choices: rock, paper, scissors"""
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        if choice.lower() not in choices:
            await ctx.send("Invalid choice! Please choose rock, paper, or scissors.")
            return

        if choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (choice.lower() == "rock" and bot_choice == "scissors") or \
             (choice.lower() == "paper" and bot_choice == "rock") or \
             (choice.lower() == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "I win!"

        await ctx.send(f"You chose {choice}, I chose {bot_choice}. {result}")

async def setup(bot):
    await bot.add_cog(RPS(bot))