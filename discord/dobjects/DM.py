class dmobj():
    def __init__(self, mainBot, dmObject, bot_id):
        """
        Variables for author
        """
        self.id = dmObject['id']
        self.last_msg_id = dmObject['last_message_id']

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot

    def send_message(self, msg):
        self.bot.send_message(self.id, msg)

    def send_embed(self, color_int, title, description, url = None, author_name = None, Image = None):
        self.bot.sendEmbed(self.id, color_int, title, description, url, author_name, Image)