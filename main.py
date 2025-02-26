# FILE: /EtheryaBot/EtheryaBot/main.py

import discord
from discord.ext import commands
import json
import os
from utils.keep_alive import keep_alive
from commands import embed, frags, pret, livret_a, entreprise, calcul, auto_clan, help

# Load configuration
with open('data/config.json') as config_file:
    config = json.load(config_file)

TOKEN = os.getenv('TOKEN_BOT_DISCORD')
GUILD_ID = config['guild_id']

# Initialize bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!!', intents=intents)

# Load commands
bot.add_cog(embed.EmbedCommands(bot))
bot.add_cog(frags.FragsCommands(bot))
bot.add_cog(pret.PretCommands(bot))
bot.add_cog(livret_a.LivretACommands(bot))
bot.add_cog(entreprise.EntrepriseCommands(bot))
bot.add_cog(calcul.CalculCommands(bot))
bot.add_cog(auto_clan.AutoClanCommands(bot))
bot.add_cog(help.HelpCommands(bot))

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

# Load JSON data
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

# Save JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Event for new member joining
@bot.event
async def on_member_join(member):
    await auto_clan.assign_role(member)

# Run the bot
keep_alive()
bot.run(TOKEN)