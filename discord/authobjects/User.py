class userobj():
    def __init__(self, userobj):
        """
        Variables for user
        """
        
        self.name = userobj['username']
        self.id = userobj['id']

        self.discriminator = userobj['discriminator']

        self.avatar = userobj['avatar']

        self.mention = '<@{}>'.format(self.id)

    @property
    def avatar_url(self):
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png"
    
    # def add_role(self, guild_id, role_id):
    #     self.bot.add_role(guild_id, self.user_id, role_id)

    # def has_role(self, role_id):
    #     return role_id in self.author_roles

    # def send_dm(self, msg):
    #     dm = self.bot.create_dm(self.user_id)
    #     dm.send_dm(msg)