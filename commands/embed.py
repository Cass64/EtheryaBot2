from discord import Embed
from discord.ext import commands
import json
import os

class EmbedCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed", description="Créer un embed personnalisé")
    async def create_embed(self, ctx, title: str, description: str):
        embed = Embed(title=title, description=description, color=0xFFFFFF)
        embed.set_footer(text="Ceci est un embed personnalisé.")
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EmbedCommand(bot))