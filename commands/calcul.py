from discord import Embed
from discord.ext import commands
import json
import os

class CalculCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calcul", description="Calcule un pourcentage d'un nombre")
    async def calcul(self, ctx, nombre: float, pourcentage: float):
        resultat = (nombre * pourcentage) / 100
        embed = Embed(
            title="📊 Calcul de pourcentage",
            description=f"{pourcentage}% de {nombre} = **{resultat}**",
            color=0x00FF00
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CalculCommands(bot))