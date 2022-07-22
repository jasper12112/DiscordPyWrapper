from discord.dobjects.Member import memberobj

class channelobj():
    def __init__(self, mainBot, channelOBJ, bot_id):
        """
        Variables for author
        """
        self.id = channelOBJ['id']
        self.name = channelOBJ['name']
        self.topic = channelOBJ['topic']
        self.guild_id = channelOBJ['guild_id']
        self.is_nsfw = channelOBJ['nsfw']
        self.rate_lim_user = channelOBJ['rate_limit_per_user']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot

    def send_message(self, msg):
        self.bot.send_message(self.id, msg)