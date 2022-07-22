from discord.dobjects.Member import memberobj

class ctx():
    def __init__(self, mainBot, messageObject, bot_id):
        """
        Variables for author
        """
        self.author_username = messageObject['d']['author']['username']
        self.author_roles = messageObject['d']['member']['roles']
        self.author_id = messageObject['d']['author']['id']
        self.mention_author = '<@{}>'.format(self.author_id)

        """
        Channel and Guild variables
        """
        self.channel_id = messageObject['d']['channel_id']
        
        self.channel = mainBot.get_channel(messageObject['d']['channel_id'])

        self.guild_id = messageObject['d']['guild_id']

        """
        Message variables
        """
        args = messageObject['d']['content'].split(' ')
        
        self.content = messageObject['d']['content']
        self.command = args[0]
        del args[0]
        self.args = args

        self.message_id = messageObject['d']['id']

        tempOBJ = {
            'user' : {
                "username": self.author_username,
                "id": self.author_id,
            },
            'roles': self.author_roles,
            'guild_id': self.guild_id,
        }

        self.member = memberobj(mainBot, tempOBJ, bot_id)

        """
        Bot related
        """
        self.bot_id = 1
        self.bot = mainBot

    def reply(self, msg):
        self.bot.send_message(self.channel_id, msg)

    def add_reaction(self, emoji):
        self.bot.add_reaction(self.channel_id, self.message_id, emoji)

    def del_msg(self):
        self.bot.delete_message(self.channel_id, self.message_id)

    def reply_embed(self, color_int, title, description, url = None, author_name = None, Image = None):
        self.bot.sendEmbed(self.channel.id, color_int, title, description, url, author_name, Image)
    
    def delete_message(self):
        self.bot.delete_message(self.channel_id, self.message_id)

    def create_dm(self):
        return self.bot.create_dm(self.author_id)