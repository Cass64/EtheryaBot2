from discord import Embed, Interaction
from discord.ext import commands
import json
import os

class EntrepriseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/entreprises.json'
        self.ensure_data_file()

    def ensure_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({}, f)

    def read_data(self):
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def write_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    @commands.command(name="constructionentreprise", description="Construire une entreprise")
    async def construction_entreprise(self, interaction: Interaction):
        user = interaction.user
        user_data = self.read_data()

        if str(user.id) in user_data and user_data[str(user.id)].get("entreprise_constructed", False):
            await interaction.response.send_message("❌ Vous avez déjà une entreprise.", ephemeral=True)
            return

        user_data[str(user.id)] = {"entreprise_constructed": True}
        self.write_data(user_data)

        embed_user = Embed(
            title="🏗️ Construction d'Entreprise",
            description=f"{user.mention}, vous avez construit une entreprise avec succès ! 🎉",
            color=0x00FF00
        )
        embed_user.set_footer(text="Bonne chance pour votre nouvelle entreprise !")

        await interaction.response.send_message(embed=embed_user, ephemeral=True)

    @commands.command(name="collectentreprise", description="Collecter les revenus de votre entreprise")
    async def collect_entreprise(self, interaction: Interaction):
        user = interaction.user
        user_data = self.read_data()

        if str(user.id) not in user_data or not user_data[str(user.id)].get("entreprise_constructed", False):
            await interaction.response.send_message("❌ Vous n'avez pas d'entreprise à collecter.", ephemeral=True)
            return

        amount = random.randint(25000, 50000)
        user_data[str(user.id)]["balance"] = user_data[str(user.id)].get("balance", 0) + amount
        self.write_data(user_data)

        embed_gain = Embed(
            title="💰 Revenus d'Entreprise",
            description=f"{user.mention}, vous avez collecté **{amount:,}** pièces grâce à votre entreprise ! 🏦",
            color=0xFFD700
        )
        embed_gain.set_footer(text="Revenez demain pour un autre retrait.")

        await interaction.response.send_message(embed=embed_gain, ephemeral=True)

    @commands.command(name="quitterentreprise", description="Quitter ou supprimer votre entreprise")
    async def quitter_entreprise(self, interaction: Interaction):
        user = interaction.user
        user_data = self.read_data()

        if str(user.id) not in user_data or not user_data[str(user.id)].get("entreprise_constructed", False):
            await interaction.response.send_message("❌ Vous n'avez pas d'entreprise à quitter.", ephemeral=True)
            return

        del user_data[str(user.id)]
        self.write_data(user_data)

        embed_user = Embed(
            title="🚫 Quitter l'Entreprise",
            description=f"{user.mention}, vous avez quitté votre entreprise avec succès.",
            color=0xFF0000
        )
        embed_user.set_footer(text="Vous pouvez revenir si vous souhaitez en construire une autre.")

        await interaction.response.send_message(embed=embed_user, ephemeral=True)

def setup(bot):
    bot.add_cog(EntrepriseCommands(bot))