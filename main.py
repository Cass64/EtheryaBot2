import discord
from discord.ext import commands
import motor.motor_asyncio
from flask import Flask
import os
import asyncio
import threading

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

COGS = ["cogs.custom_commands", "cogs.moderation", "cogs.economy", "cogs.images"]

@bot.event
async def on_ready():
    print("🟢 on_ready() s'exécute !")
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    print(f"🔗 Connecté à {len(bot.guilds)} serveurs")
    print("🚀 Le bot est prêt à l'emploi !")

def run_flask():
    print("🌐 Démarrage de Flask...")
    app.run(host="0.0.0.0", port=port)

async def run_bot():
    print("🚀 Lancement de run_bot()...")

    TOKEN = os.getenv('TOKEN_BOT_DISCORD')

    if not TOKEN:
        print("❌ ERREUR: La variable d'environnement TOKEN_BOT_DISCORD n'est pas définie !")
        return  # Arrête l'exécution si le token est manquant

    print(f"🔑 Token détecté: {TOKEN[:10]}... (masqué)")  # Affiche un bout du token pour voir s'il est bien chargé

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
        print("❌ ERREUR: Le token est invalide ! Vérifie la clé dans tes variables d'environnement.")
    except Exception as e:
        print(f"❌ ERREUR INATTENDUE: {e}")


if __name__ == "__main__":
    print("🟠 Démarrage du script principal...")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("🟡 Exécution de run_bot()...")
    
    loop.run_until_complete(run_bot())


