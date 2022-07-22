class roleobj():
    def __init__(self, mainBot, roleObject, bot_id):
        """
        Variables for author
        """
        self.name = roleObject['name']
        self.id = roleObject['id']
        self.mentionable = roleObject['mentionable']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot