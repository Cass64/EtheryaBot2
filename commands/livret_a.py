from discord import Embed
from discord.ext import commands
import json
import os

class LivretACommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/livret_a.json'
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

    @commands.command(name="investirlivreta")
    async def investir_livret(self, ctx, montant: int):
        if montant <= 0 or montant > 100000:
            await ctx.send("❌ Montant invalide. Veuillez entrer un montant entre 1 et 100,000.")
            return

        user_id = str(ctx.author.id)
        data = self.read_data()
        current_balance = data.get(user_id, 0)
        new_balance = current_balance + montant
        data[user_id] = new_balance
        self.write_data(data)

        embed = Embed(
            title="📥 Investissement - Livret A",
            description=f"{ctx.author.mention} a investi **{montant}** 💰 dans son Livret A !\n💰 Total : **{new_balance}**",
            color=0x00FF00
        )
        await ctx.send(embed=embed)

    @commands.command(name="livreta")
    async def consulter_livret(self, ctx):
        user_id = str(ctx.author.id)
        data = self.read_data()
        balance = data.get(user_id, 0)

        embed = Embed(
            title="📈 Solde du Livret A",
            description=f"💰 Votre solde actuel : **{balance}** crédits",
            color=0x00FF00
        )
        embed.set_footer(text="Les intérêts sont ajoutés chaque semaine (+2%).")
        await ctx.send(embed=embed)

    @commands.command(name="retirerlivreta")
    async def retirer_livret(self, ctx, montant: int = None):
        user_id = str(ctx.author.id)
        data = self.read_data()
        current_balance = data.get(user_id, 0)

        if current_balance == 0:
            await ctx.send("❌ Vous n'avez pas d'argent dans votre Livret A.")
            return

        montant_max = current_balance
        montant = montant if montant is not None else montant_max

        if montant <= 0 or montant > montant_max:
            await ctx.send(f"❌ Vous pouvez retirer entre **1 et {montant_max}** 💰.")
            return

        new_balance = current_balance - montant
        data[user_id] = new_balance
        self.write_data(data)

        embed = Embed(
            title="💸 Demande de Retrait - Livret A",
            description=f"{ctx.author.mention} a retiré **{montant}** 💰 de son Livret A.\n💰 Nouveau solde : **{new_balance}**",
            color=0xFFA500
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LivretACommands(bot))