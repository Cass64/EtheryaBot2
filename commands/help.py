from discord import Embed
from discord.ext import commands
import json
import os

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(HelpCommands(bot))