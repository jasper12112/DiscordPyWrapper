from discord.dobjects.Channel import channelobj
from discord.websocket import _app as websocket
import json
import threading
import requests

import time

from discord.dobjects.Context import ctx
from discord.dobjects.Member import memberobj
from discord.dobjects.Role import roleobj
from discord.dobjects.Reaction import reactionobj
from discord.dobjects.Invite import inviteobj
from discord.dobjects.DM import dmobj

class Client:
    def __init__(self):
        self.token = 'token'
        self.heartbeatInterval = 41250
        self.id = 11
        self.session_id = 55
        self.last_seq = None
        self.t = None
        self.prefix = '!'

        self.commands = []

    def start(self, token, prefix = '!'):
        self.token = token
        self.headers = { "Authorization":"Bot {}".format(self.token),
        "User-Agent":"myBotThing (http://some.url, v0.1)",
        "Content-Type":"application/json", }
        self.getMyID()
        self.connect_socket()
        self.prefix = prefix

    def message_rec(self, ws, message):
        msg_json = json.loads(message)
        opcode = msg_json['op']

        self.last_seq = msg_json['s']
        if opcode == 10:
            self.heartbeatInterval = msg_json["d"]["heartbeat_interval"]
            self.heartbeatHello()
        elif msg_json['t'] == "MESSAGE_CREATE":
            if msg_json['d']['author']['id'] != self.id:
                ctxObject = ctx(self, msg_json, self.id)
                for comm in self.commands:
                    if '!' + comm[0] == ctxObject.command:
                        comm[1](ctxObject)
                        self.on_log(ctxObject)
                        return
                self.on_message(ctxObject)
                self.on_log(ctxObject)

        elif msg_json['t'] == "GUILD_MEMBER_ADD":
            self.on_member_join(memberobj(self, msg_json['d'], self.id))

        elif msg_json['t'] == "MESSAGE_REACTION_ADD":
            self.on_reaction(reactionobj(self, msg_json['d'], self.id))
        elif opcode == 0:
            if msg_json['d']['session_id'] == None:
                print('no session id')
                self.ws.close()
                self.connect_socket()
                self.resume()
            else:
                self.session_id = msg_json["d"]["session_id"]
        elif opcode == 1:
            if self.t != None:
                self.t.cancel()
            self.heartbeatHello()
        elif opcode == 7:
            print("Opcode 7, need to resume connection!")
            if self.t != None:
                self.t.cancel()
            self.ws.close()
            self.connect_socket()
            self.resume()
        elif opcode == 9:
            print("Print opcode 9, fatal error. Resumming connection!")
            if self.t != None:
                self.t.cancel()
            self.ws.close()
            self.connect_socket()
            self.resume()

    def on_message(self, ctx):
        pass

    def on_log(self, ctx):
        pass

    def on_ready(self):
        pass

    def on_reaction(self, reaction):
        pass

    def on_member_join(self, member):
        pass

    def on_error(self, ws, error):
        print("Got a error.")
        if self.t != None:
            self.t.cancel()
        self.ws.close()
        self.connect_socket()
        self.resume()

    def on_close(self, ws):
        print("Reconneting...")
        if self.t != None:
            self.t.cancel()
        self.ws.close()
        self.connect_socket()
        self.resume()

    def connect_socket(self):
        self.ws = None
        self.ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=6&encoding=json", on_message= self.message_rec, on_error = self.on_error, on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.on_ready()
        self.ws.run_forever()

    def resume(self):
        print("Resuming")
        p_json = json.dumps({"op": 6,"d": {"token": self.token,"session_id": self.session_id,"seq": self.last_seq}})
        self.ws.send(p_json)

    def heartbeatHello(self):
        self.t = threading.Timer(self.heartbeatInterval / 1000, self.heartbeatHello).start()
        heartbeat_json = json.dumps({"op": 1,"d": 251})
        try:
            self.ws.send(heartbeat_json)
        except:
            if self.t != None:
                self.t.cancel()
            self.ws.close()
            self.connect_socket()
            self.resume()

    def on_open(self, ws):
        p_json = json.dumps({"op": 2,"d": {"token": self.token,"intents": 1871,"properties": {"$os": "linux","$browser": "my_library","$device": "my_library"}},"compress": "false","presence": {"game": {},"status": "online","since": "null","afk": "false"}})
        self.ws.send(p_json)


    ###HTTP REQUESTS###
    def getMyID(self):
        baseURL = "https://discordapp.com/api/users/@me"
        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)
        print(request_json)
        self.id = request_json['id']

    def get_channel(self, channel_id):
        baseURL = "https://discordapp.com/api/channels/{}".format(channel_id)

        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)
        
        return channelobj(self, request_json, self.id)

    def send_message(self, id, msg):
        baseURL = "https://discordapp.com/api/channels/{}/messages".format(id)

        POSTedJSON =  json.dumps ( {"content":msg} )
        r = requests.post(baseURL, headers = self.headers, data = POSTedJSON)

    def editMessage(self, channel_id, message_id, msg):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}".format(channel_id, message_id)

        POSTedJSON =  json.dumps ( {"content":msg} )

        requests.patch(baseURL, headers = self.headers, data = POSTedJSON)

    def get_guild_member(self, guild_id, user_id):
        baseURL = "https://discordapp.com/api/guilds/{}/members/{}".format(guild_id, user_id)

        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)

        return memberobj(self, request_json, self.id)


    def add_reaction(self, channel_id, message_id, emoji):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}/reactions/{}/@me".format(channel_id, message_id, emoji)

        requests.put(baseURL, headers = self.headers)

    #Get a list of users that reacted with a specific emoji
    def get_reactions(self, guild_id, channel_id, message_id, emoji):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}/reactions/{}".format(channel_id, message_id, emoji)

        r = requests.get(baseURL, headers = self.headers)

        request_json = json.loads(r.text)

        users = []

        for user in request_json:
            users.append(self.get_guild_member(guild_id, user['id']))

        return users

    def delete_reaction(self, channel_id, message_id, emoji, user_id):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}/reactions/{}/{}".format(channel_id, message_id, emoji, user_id)
        requests.delete(baseURL, headers = self.headers)

    def delete_all_reactions(self, channel_id, message_id):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}/reactions".format(channel_id, message_id)
        requests.delete(baseURL, headers = self.headers)

    def delete_all_reactions_emoji(self, channel_id, message_id, emoji):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}/reactions/{}".format(channel_id, message_id, emoji)
        requests.delete(baseURL, headers = self.headers)

    def delete_message(self, channel_id, message_id):
        baseURL = "https://discordapp.com/api/channels/{}/messages/{}".format(channel_id, message_id)
        requests.delete(baseURL, headers = self.headers)

    def delete_messages(self, channel_id, amount = 50):
        baseMessagesURI = 'https://discordapp.com/api/channels/{}/messages?limit={}'.format(channel_id, amount)
        r = requests.get(baseMessagesURI, headers = self.headers)
        request_json = json.loads(r.text)

        message_ids = []

        for messages in request_json:
            message_ids.append(messages["id"])

        print(message_ids)

        baseURL = 'https://discordapp.com/api/channels/{}/messages/bulk-delete'.format(channel_id)

        postedJson = json.dumps ({"messages" : message_ids})

        requests.post(baseURL, headers = self.headers, data = postedJson)

    def sendEmbed(self, channel_id, color_int, title, description, url = None, author_name = None, Image = None):
        #int 838308

        baseURL = "https://discordapp.com/api/channels/{}/messages".format(channel_id)

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


    def get_guild_members(self, guild_id):
        baseURL = "https://discordapp.com/api/guilds/{}/members?limit=1000".format(guild_id)

        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)

        member_list = []
        for member in request_json:
            member_list.append(memberobj(self, member, self.id))

        return member_list
    
    #Returns a member by name
    def search_guild_member(self, guild_id, name):
        baseURL = "https://discordapp.com/api/guilds/{}/members/search?query={}".format(guild_id, name)

        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)

        member = memberobj(self, request_json, self.id)

        return member

    def get_guilds(self):
        baseURL = "https://discordapp.com/api/users/@me/guilds"

        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)
        return request_json

    def add_role(self, guild_id, user_id, role_id):    
        baseURL = "https://discordapp.com/api/guilds/{}/members/{}/roles/{}".format(guild_id, user_id, role_id)
        requests.put(baseURL, headers = self.headers)

    def remove_role_member(self, guild_id, user_id, role_id):    
        baseURL = "https://discordapp.com/api/guilds/{}/members/{}/roles/{}".format(guild_id, user_id, role_id)
        requests.delete(baseURL, headers = self.headers)

    def kick_member(self, guild_id, user_id):
        baseURL = "https://discordapp.com/api/guilds/{}/members/{}".format(guild_id, user_id)
        requests.delete(baseURL, headers = self.headers)

    def ban_member(self, guild_id, user_id, reason):
        baseURL = "https://discordapp.com/api/guilds/{}/bans/{}".format(guild_id, user_id)

        POSTedJSON =  json.dumps ( {
            "reason": reason
        } )

        requests.put(baseURL, headers = self.headers, data = POSTedJSON)

    def unban_member(self, guild_id, user_id):
        baseURL = "https://discordapp.com/api/guilds/{}/bans/{}".format(guild_id, user_id)

        requests.delete(baseURL, headers = self.headers)

    def get_guild_roles(self, guild_id):
        baseURL = "https://discordapp.com/api/guilds/{}/roles".format(guild_id)
        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)

        guildRolesList = []

        for guildOBJ in request_json:
            guildRolesList.append(roleobj(self, guildOBJ, self.id))

        return guildRolesList

    #returns a role
    def get_role(self, guild_id, role_name):
        guildRolesList = self.get_guild_roles(guild_id)

        for role in guildRolesList:
            if role.name == role_name:
                return role
                break
        return None

    def get_user(self, user_id):
        baseURL = 'https://discordapp.com/api/users/{}'.format(user_id)
        r = requests.get(baseURL, headers = self.headers)
        request_json = json.loads(r.text)

        memb = {
            'user': {
                'username': request_json["username"],
                'id': request_json["id"],
            }
        }

        return memb

    def remove_role(self, guild_id, role_id):
        baseURL = "https://discordapp.com/api/guilds/{}/roles/{}".format(guild_id, role_id)

        requests.delete(baseURL, headers = self.headers)

    #Returns a invite object (max (age,uses) 0 = forever, age is in seconds. uses is how many uses (INT))
    def create_channel_invite(self, channel_id, max_age, max_uses):
        baseURL = "https://discordapp.com/api/channels/{}/invites".format(channel_id)

        PostedJSON = json.dumps({
            "max_age": int(max_age),
            "max_uses": int(max_uses),
        })

        r = requests.post(baseURL, headers = self.headers, data = PostedJSON)

        request_json = json.loads(r.text)

        return inviteobj(self, request_json, self.id)

    #Returns a list of invite objects
    def get_channel_invites(self, channel_id):
        baseURL = "https://discordapp.com/api/channels/{}/invites".format(channel_id)

        r = requests.get(baseURL, headers = self.headers)

        request_json = json.loads(r.text)

        print(request_json)

        inviteList = []

        for inviteb in request_json:
            inviteList.append(inviteobj(self, inviteb, self.id))

        return inviteList

    def create_dm(self, user_id):
        baseURL = "https://discordapp.com/api/users/@me/channels"

        POSTedJSON =  json.dumps ( {
            "recipient_id": user_id
        } )

        r = requests.post(baseURL, headers = self.headers, data=POSTedJSON)
        
        request_json = json.loads(r.text)

        return dmobj(self, request_json, self.id)

    ##EVENT FUNCTION BINDER##
    def event(self):

        def inner(function):
            setattr(self, function.__name__, function)
        return inner

    ##COMMAND FUNCTION BINDER##
    def command(self, *args, **kwargs):

        def inner(function):      
            if 'alias' in kwargs:
                for alias in kwargs['alias']:
                    self.commands.append([alias, function])
            self.commands.append([function.__name__, function])

        return inner