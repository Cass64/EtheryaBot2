from discord import Embed
from discord.ext import commands
import json
import os

class PretCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/prets.json'
        self.ensure_data_file()

    def ensure_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({}, f)

    def load_data(self):
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    @commands.command(name="pret")
    async def pret(self, ctx, membre: str, montant: int, montant_a_rendre: int, duree: str):
        data = self.load_data()
        if membre not in data:
            data[membre] = {
                "montant": montant,
                "montant_a_rendre": montant_a_rendre,
                "duree": duree,
                "statut": "En Cours"
            }
            self.save_data(data)

            embed = Embed(
                title="📜 Nouveau Prêt",
                description=f"Prêt de **{montant}** crédits accordé à {membre}.",
                color=0x00ff00
            )
            embed.add_field(name="💰 Montant à rendre", value=f"{montant_a_rendre} crédits", inline=False)
            embed.add_field(name="📅 Durée", value=duree, inline=False)
            embed.set_footer(text="Prêt enregistré avec succès.")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Un prêt est déjà en cours pour {membre}.")

    @commands.command(name="terminer")
    async def terminer(self, ctx, membre: str):
        data = self.load_data()
        if membre in data:
            del data[membre]
            self.save_data(data)

            embed = Embed(
                title="✅ Prêt Terminé",
                description=f"Le prêt pour {membre} a été marqué comme terminé.",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Aucun prêt trouvé pour {membre}.")

def setup(bot):
    bot.add_cog(PretCommands(bot))