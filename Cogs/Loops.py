import asyncio
import os
from datetime import datetime
from discord.ext import commands, tasks
from Utilities import Functions


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_user_id = int(os.getenv('MY_DISCORD_USER_ID'))
        self.target_user = self.bot.get_user(self.target_user_id)

    @tasks.loop(minutes=5)
    async def clock(self):
        if not self.target_user:
            self.target_user = self.bot.get_user(self.target_user_id)
        await Functions.check_energy_or_nerve_reach_levels(self.target_user, 0.75)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.clock.is_running():
            self.clock.start()

    @clock.before_loop
    async def before_clock(self):
        for _ in range(86400):
            # If current minute has no remainder after being divided by 5, ie 5, 10, 15, 20,
            # and the current second is 0, start loop
            if not datetime.utcnow().minute % 5 and datetime.utcnow().second == 0:
                return
            await asyncio.sleep(1)  # Wait 1 second and try again


# run when load_extension() is called
def setup(bot):
    bot.add_cog(Loops(bot))



