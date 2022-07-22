import requests
import json

class dmobj():
    def __init__(self, dmObject, headers):
        """
        Variables for author
        """
        self.id = dmObject['id']
        self.last_msg_id = dmObject['last_message_id']

        self.headers = headers


    def send_message(self, msg):
        baseURL = "https://discordapp.com/api/channels/{}/messages".format(id)

        POSTedJSON =  json.dumps ( {"content":msg} )

        requests.post(baseURL, headers = self.headers, data = POSTedJSON)

    def send_embed(self, color_int, title, description, url = None, author_name = None, Image = None):
        baseURL = "https://discordapp.com/api/channels/{}/messages".format(self.id)

        if Image == None:
            Image = ''

        if author_name:
            POSTedJSON =  json.dumps ( {"embed":{
                "color": color_int,
                "author": {
                "name": author_name,
                },
                "title": title,
                "url": url,
                "description": description,
                "image": {"url": Image},
            }} )
        else:
            POSTedJSON =  json.dumps ( {"embed":{
                "color": color_int,
                "title": title,
                "url": url,
                "description": description,
                "image": {"url": Image},

            }} )

        requests.post(baseURL, headers = self.headers, data = POSTedJSON)