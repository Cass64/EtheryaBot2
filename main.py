import discord
from discord.ext import commands
import motor.motor_asyncio
from flask import Flask
import os
import threading

app = Flask(__name__)

# Utilise la variable d'environnement PORT fournie par Render
port = int(os.getenv('PORT', 5000))  # Défaut à 5000 si non définie

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

def run_flask():
    # Exécution de Flask sur un thread séparé
    app.run(host='0.0.0.0', port=port)

async def run_bot():
    # Charger les cogs
    for cog in COGS:
        await bot.load_extension(cog)
    
    await bot.start(os.getenv("TOKEN_BOT_DISCORD"))

if __name__ == "__main__":
    # Démarrer Flask dans un thread séparé
    threading.Thread(target=run_flask).start()

    # Démarrer le bot Discord
    run_bot()
