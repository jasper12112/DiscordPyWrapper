class inviteobj():
    def __init__(self, mainBot, invobject, bot_id):
        """
        Variables for author
        """
        self.code = invobject['code']

        self.guild_id = invobject['guild']['id']
        self.guild_name = invobject['guild']['name']

        self.channel_id = invobject['channel']['id']
        self.channel_name = invobject['channel']['name']

        self.max_uses = invobject['max_uses']
        self.max_age = invobject['max_age']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot