import discord
from discord.ext import commands
import motor.motor_asyncio
from flask import Flask
import os
import asyncio
import threading
import requests  # Pour tester la connexion API Discord

app = Flask(__name__)

@app.route('/')
def index():
    return "Le bot fonctionne !"

port = int(os.getenv('PORT', 5000))  # Port utilisé pour Flask

# Connexion à MongoDB
MONGO_URL = os.getenv("MONGO_URI")
if not MONGO_URL:
    print("❌ ERREUR: La variable d'environnement MONGO_URI n'est pas définie !")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Cass-Eco2"]

# Configuration des intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!!", intents=intents)

# Ajout du client MongoDB en tant qu'attribut du bot
bot.mongo_client = mongo_client  # C'est ici que tu l'ajoutes

COGS = ["cogs.custom_commands", "cogs.moderation", "cogs.economy", "cogs.images"]

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    print(f"🔗 Connecté à {len(bot.guilds)} serveurs")
    print("🚀 Le bot est prêt à l'emploi !")

# Test de la connexion à l'API Discord avant de démarrer le bot
print("🟢 Test de connexion à l'API Discord en cours...")

try:
    response = requests.get("https://discord.com/api/v10/gateway")
    if response.status_code == 200:
        print("✅ Render peut accéder à l'API Discord.")
    else:
        print(f"❌ Render ne peut pas accéder à Discord. Code: {response.status_code}")
except Exception as e:
    print(f"❌ Erreur de connexion à Discord: {e}")

def run_flask():
    print("🟢 Démarrage de Flask...")
    app.run(host="0.0.0.0", port=port)

async def run_bot():
    print("🟡 Tentative de démarrer le bot...")
    TOKEN = os.getenv("TOKEN_BOT_DISCORD")

    if not TOKEN:
        print("❌ ERREUR: La variable d'environnement TOKEN_BOT_DISCORD n'est pas définie !")
        return

    print(f"🔑 Token détecté: {TOKEN[:10]}... (masqué)")

    # Charger les COGS avec gestion des erreurs
    i = 0
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            i += 1
            print(f"✅ Cog {i} chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {cog}: {e}")

    print("🔄 Démarrage du bot...")
    try:
        await bot.start(TOKEN)
    except discord.LoginFailure:
        print("❌ ERREUR: Le token est invalide !")
    except Exception as e:
        print(f"❌ ERREUR INATTENDUE: {e}")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    loop = syncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(run_bot())

