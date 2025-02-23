import discord
from discord.ext import commands
import motor.motor_asyncio
from flask import Flask
import os
import asyncio
import threading

app = Flask(__name__)

# Route Flask pour tester
@app.route('/')
def index():
    return "Le bot fonctionne !"

# Utilise la variable d'environnement PORT fournie par Render
port = int(os.getenv('PORT', 5000))  # Défaut à 5000 si non défini

# Connexion à MongoDB
MONGO_URL = os.getenv("MONGO_URI")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Cass-Eco2"]

# Configuration du bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ajout de l'intent de contenu de message

bot = commands.Bot(command_prefix="!!", intents=intents)

# Chargement des cogs
bot.mongo_client = mongo_client  # Ajoute le client MongoDB au bot
COGS = ["cogs.custom_commands", "cogs.moderation", "cogs.economy", "cogs.images"]

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

async def run_flask():
    # Exécution de Flask sur un thread séparé en utilisant asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, app.run, '0.0.0.0', port)

async def run_bot():
    # Charger les cogs de manière asynchrone
    for cog in COGS:
        await bot.load_extension(cog)  # Utiliser await ici
    
    # Démarrer le bot
    await bot.start(os.getenv("TOKEN_BOT_DISCORD"))

if __name__ == "__main__":
    # Démarrer Flask et le bot Discord simultanément dans asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(run_flask())  # Flask dans un task
    loop.run_until_complete(run_bot())  # Démarre le bot Discord
