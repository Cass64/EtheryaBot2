import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_custom_role(self, ctx):
        """Vérifie si l'utilisateur a le rôle 'AdminMod'."""
        role = discord.utils.get(ctx.guild.roles, name="″ [𝑺ץ] Développeur") 
        if role and role in ctx.author.roles:
            return True
        return False

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Bannir un membre."""
        if not self.has_custom_role(ctx):
            return await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} a été banni pour : {reason}")

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Expulser un membre."""
        if not self.has_custom_role(ctx):
            return await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} a été expulsé pour : {reason}")

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        """Mute un membre en lui ajoutant un rôle 'Muted'."""
        if not self.has_custom_role(ctx):
            return await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
        
        await member.add_roles(role)
        await ctx.send(f"{member.name} a été mute.")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        """Unmute un membre."""
        if not self.has_custom_role(ctx):
            return await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"{member.name} a été unmute.")
        else:
            await ctx.send("Ce membre n'est pas mute.")

async def setup(bot):
    bot.add_cog(Moderation(bot))
