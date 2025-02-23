import discord
from discord.ext import commands
form flask import Flask
import motor.motor_asyncio
import os

app = Flask(__name__)

# Utilise la variable d'environnement PORT fournie par Render
port = int(os.getenv('PORT', 5000))  # Défaut à 5000 si non définie

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv("TOKEN_BOT_DISCORD")  # Le token sera stocké sur Render

# Connexion à MongoDB
MONGO_URL = os.getenv("MONGO_URI")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Cass-Eco2"]

# Configuration du bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!!", intents=intents)

# Chargement des cogs
COGS = ["cogs.custom_commands", "cogs.moderation", "cogs.economy", "cogs.images"]

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)
    
    bot.run(TOKEN)
