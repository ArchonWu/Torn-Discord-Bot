import json
import discord

from discord.ext import commands

from Utilities import Functions
from enum import Enum


class Stat(Enum):
    ENERGY = "energy"
    NERVE = "nerve"
    HAPPY = "happy"
    LIFE = "life"


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Display bars (e.g. energy, nerve)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):

        # Acknowledge receipt of the command
        await ctx.defer()

        # API call
        user_all_stats = await Functions.request_all_player_stats()

        if not user_all_stats:
            return await ctx.respond("No response from the API", "Error")

        if "error" in user_all_stats:
            return await ctx.respond("Error in the API call")

        embed = discord.Embed(title=f"Your Stats", color=discord.Color.blue())
        for stat in Stat:
            stat_curr = user_all_stats[stat.value]["current"]
            stat_max = user_all_stats[stat.value]["maximum"]
            embed.add_field(name=stat.value.capitalize(),
                            value=f"{stat_curr} / {stat_max}",
                            inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
