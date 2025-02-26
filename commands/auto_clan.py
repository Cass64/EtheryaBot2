from discord.ext import commands
import discord
import random
import json
import os

# Load configuration
with open('data/config.json') as f:
    config = json.load(f)

# Load roles from the configuration
roles_to_assign = config.get("roles_to_assign", [])

class AutoClan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        existing_roles = [role.name for role in member.roles]
        if not any(role in roles_to_assign for role in existing_roles):
            role_name = random.choice(roles_to_assign)
            role = discord.utils.get(member.guild.roles, name=role_name)
            
            if role:
                await member.add_roles(role)
                embed = discord.Embed(
                    title="🎉 Un nouveau membre rejoint !",
                    description=f"{member.mention} vient de rejoindre le serveur et a été assigné au rôle **{role_name}**.",
                    color=discord.Color.white()
                )
                embed.set_footer(text="Bienvenue parmi nous !")
                
                channel = self.bot.get_channel(config.get("welcome_channel_id"))
                if channel:
                    await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(AutoClan(bot))