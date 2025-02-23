import discord
from discord.ext import commands
from pymongo import MongoClient

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient("mongodb://localhost:27017")  # URL de connexion MongoDB
        self.db = self.client["bot_database"]  # Nom de la base de données
        self.collection = self.db["custom_commands"]  # Nom de la collection

    async def get_custom_commands(self, guild_id):
        """Récupère les commandes personnalisées pour un serveur donné."""
        guild_data = self.collection.find_one({"guild_id": guild_id})
        if guild_data:
            return guild_data["commands"]
        return []

    def check_permissions(self, user, required_permission):
        """Vérifie si l'utilisateur a les permissions nécessaires pour exécuter la commande."""
        if required_permission == "ADMINISTRATOR" and user.guild_permissions.administrator:
            return True
        if required_permission == "MODERATOR" and any(role.name == "Modérateur" for role in user.roles):
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Récupérer les commandes personnalisées pour ce serveur
        custom_commands = await self.get_custom_commands(str(message.guild.id))

        for cmd in custom_commands:
            # Vérifier si le message correspond à une commande personnalisée
            if message.content.startswith(cmd["name"]):
                # Vérifier les permissions
                if self.check_permissions(message.author, cmd["permissions"]):
                    await message.channel.send(cmd["response"])
                else:
                    await message.channel.send("❌ Vous n'avez pas la permission d'exécuter cette commande.")
                return

    @commands.command()
    async def addcustomcmd(self, ctx, name: str, response: str, permissions: str):
        """Commande pour ajouter une commande personnalisée."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Vous devez être administrateur pour ajouter une commande personnalisée.")

        guild_id = str(ctx.guild.id)
        new_command = {
            "name": name,
            "response": response,
            "permissions": permissions
        }

        # Ajouter la commande personnalisée à la base de données
        existing_data = self.collection.find_one({"guild_id": guild_id})
        if existing_data:
            self.collection.update_one({"guild_id": guild_id}, {"$push": {"commands": new_command}})
        else:
            self.collection.insert_one({"guild_id": guild_id, "commands": [new_command]})

        await ctx.send(f"Commande personnalisée `{name}` ajoutée avec succès.")

    @commands.command()
    async def editcustomcmd(self, ctx, old_name: str, new_name: str, new_response: str, new_permissions: str):
        """Commande pour modifier une commande personnalisée existante."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Vous devez être administrateur pour modifier une commande personnalisée.")

        guild_id = str(ctx.guild.id)
        guild_data = self.collection.find_one({"guild_id": guild_id})

        if not guild_data:
            return await ctx.send("❌ Aucune commande personnalisée trouvée pour ce serveur.")

        # Trouver la commande à modifier
        command_to_edit = None
        for cmd in guild_data["commands"]:
            if cmd["name"] == old_name:
                command_to_edit = cmd
                break

        if command_to_edit:
            # Modifier les détails de la commande
            self.collection.update_one(
                {"guild_id": guild_id, "commands.name": old_name},
                {"$set": {"commands.$.name": new_name, "commands.$.response": new_response, "commands.$.permissions": new_permissions}}
            )
            await ctx.send(f"Commande `{old_name}` modifiée avec succès en `{new_name}`.")
        else:
            await ctx.send(f"❌ Aucune commande personnalisée trouvée avec le nom `{old_name}`.")

    @commands.command()
    async def deletecustomcmd(self, ctx, name: str):
        """Commande pour supprimer une commande personnalisée."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Vous devez être administrateur pour supprimer une commande personnalisée.")

        guild_id = str(ctx.guild.id)
        guild_data = self.collection.find_one({"guild_id": guild_id})

        if not guild_data:
            return await ctx.send("❌ Aucune commande personnalisée trouvée pour ce serveur.")

        # Trouver la commande à supprimer
        command_to_delete = None
        for cmd in guild_data["commands"]:
            if cmd["name"] == name:
                command_to_delete = cmd
                break

        if command_to_delete:
            # Supprimer la commande de la base de données
            self.collection.update_one(
                {"guild_id": guild_id},
                {"$pull": {"commands": {"name": name}}}
            )
            await ctx.send(f"Commande `{name}` supprimée avec succès.")
        else:
            await ctx.send(f"❌ Aucune commande personnalisée trouvée avec le nom `{name}`.")

def setup(bot):
    bot.add_cog(CustomCommands(bot))
