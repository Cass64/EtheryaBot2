from discord.ext import commands
import json
import os

class FragsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/frags.json'
        self.ensure_data_file()

    def ensure_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({}, f)

    def load_frags(self):
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def save_frags(self, frags):
        with open(self.data_file, 'w') as f:
            json.dump(frags, f)

    @commands.command(name='add_frag')
    async def add_frag(self, ctx, member: commands.MemberConverter, frag_count: int):
        frags = self.load_frags()
        user_id = str(member.id)

        if user_id not in frags:
            frags[user_id] = 0

        frags[user_id] += frag_count
        self.save_frags(frags)

        await ctx.send(f"{frag_count} frags added to {member.mention}. Total frags: {frags[user_id]}")

    @commands.command(name='get_frags')
    async def get_frags(self, ctx, member: commands.MemberConverter):
        frags = self.load_frags()
        user_id = str(member.id)

        if user_id in frags:
            await ctx.send(f"{member.mention} has {frags[user_id]} frags.")
        else:
            await ctx.send(f"{member.mention} has no frags recorded.")

def setup(bot):
    bot.add_cog(FragsCommands(bot))