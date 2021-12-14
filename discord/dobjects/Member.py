class memberobj():
    def __init__(self, mainBot, memberObject, bot_id):
        """
        Variables for author
        """
        
        self.name = memberObject['user']['username']
        self.user_id = memberObject['user']['id']

        self.author_roles = memberObject['roles']
            
        if 'guild_id' in memberObject:
            self.guild_id = memberObject['guild_id']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot
        self.mention = '<@{}>'.format(self.user_id)
    
    def add_role(self, guild_id, role_id):
        self.bot.add_role(guild_id, self.user_id, role_id)

    def has_role(self, role_id):
        return role_id in self.author_roles

    def send_dm(self, msg):
        dm = self.bot.create_dm(self.user_id)
        dm.send_dm(msg)