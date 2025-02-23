import discord
from discord.ext import commands
import motor.motor_asyncio

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.mongo_client["Cass-Eco2"]
        self.economy_collection = self.db["economy"]

    async def Eget_balance(self, user_id):
        """Récupère le solde d'un utilisateur."""
        user = await self.economy_collection.find_one({"user_id": user_id})
        if not user:
            await self.economy_collection.insert_one({"user_id": user_id, "balance": 0})
            return 0
        return user["balance"]

    async def Eupdate_balance(self, user_id, amount):
        """Met à jour le solde d'un utilisateur."""
        await self.economy_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"balance": amount}},
            upsert=True
        )

    @commands.command()
    async def Ebalance(self, ctx):
        """Affiche le solde de l'utilisateur."""
        balance = await self.get_balance(ctx.author.id)
        await ctx.send(f"💰 {ctx.author.mention}, tu as {balance} pièces.")

    @commands.command()
    async def Egive(self, ctx, member: discord.Member, amount: int):
        """Donner de l'argent à un autre membre."""
        if amount <= 0:
            return await ctx.send("Le montant doit être positif.")
        
        user_balance = await self.get_balance(ctx.author.id)
        if user_balance < amount:
            return await ctx.send("Tu n'as pas assez d'argent.")

        await self.update_balance(ctx.author.id, -amount)
        await self.update_balance(member.id, amount)
        await ctx.send(f"💸 {ctx.author.mention} a donné {amount} pièces à {member.mention}.")

def setup(bot):
    bot.add_cog(Economy(bot))
