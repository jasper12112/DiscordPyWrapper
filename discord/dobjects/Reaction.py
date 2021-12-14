class reactionobj():
    def __init__(self, mainBot, reaction, bot_id):
        """
        Variables for author
        """
        self.name = reaction['member']['user']['username']
        self.author_roles = reaction['member']['roles']
        self.user_id = reaction['member']['user']['id']
        self.message_id = reaction['message_id']
        self.emoji = reaction['emoji']['name']
        self.channel_id = reaction['channel_id']
        self.guild_id = reaction['guild_id']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot
    
    def add_role(self, guild_id, role_id):
        self.bot.add_role(guild_id, self.user_id, role_id)

    def has_role(self, role_id):
        return role_id in self.author_roles