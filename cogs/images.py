import discord
from discord.ext import commands
import motor.motor_asyncio

class Images(commands.Cog):
    def __init__(self, bot, mongo_client):
        self.bot = bot
        self.mongo_client = mongo_client["Cass-Eco2"]

    async def get_image(self, guild_id, image_name):
        """Récupère une image stockée dans la base de données."""
        return await self.images_collection.find_one({"guild_id": guild_id, "name": image_name})

    @commands.command()
    async def image(self, ctx, image_name: str):
        """Envoie une image prédéfinie ou personnalisée."""
        image_data = await self.get_image(ctx.guild.id, image_name)
        if image_data:
            await ctx.send(image_data["url"])
        else:
            await ctx.send("❌ Image introuvable.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_image(self, ctx, image_name: str, image_url: str):
        """Ajoute une image personnalisée pour le serveur."""
        existing = await self.get_image(ctx.guild.id, image_name)
        if existing:
            return await ctx.send("❌ Une image avec ce nom existe déjà.")

        await self.images_collection.insert_one({
            "guild_id": ctx.guild.id,
            "name": image_name,
            "url": image_url
        })
        await ctx.send(f"✅ Image {image_name} ajoutée avec succès.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_image(self, ctx, image_name: str):
        """Supprime une image personnalisée."""
        result = await self.images_collection.delete_one({"guild_id": ctx.guild.id, "name": image_name})
        if result.deleted_count:
            await ctx.send(f"✅ Image {image_name} supprimée.")
        else:
            await ctx.send("❌ Aucune image trouvée avec ce nom.")

async def setup(bot):
    mongo_client = bot.mongo_client
    await bot.add_cog(Images(bot, mongo_client))
