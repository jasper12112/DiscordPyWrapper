from flask import Flask, render_template, request, jsonify, session, redirect, flash
from threading import Thread
import json
import requests

from DMOBJ import dmobj
from decouple import config
from discord import DiscordOath


import os

warzone_role_id = '897414185342873630'
minecraft_role_id = '897186712806109265'
ark_role_id = '897186787653459969'
rust_role_id = '897186820096426025'
csgo_role_id = '897186862618267708'
roblox_role_id = '897187127002021899'

game_roles = {'warzone': warzone_role_id,
'minecraft': minecraft_role_id,
'ark': ark_role_id,
'rust': rust_role_id,
'csgo': csgo_role_id,
'roblox': roblox_role_id
}

token = config('DISCORD_BOT_SECRET')
client_sc = config('DISCORD_CLIENT_SECRET')
discord_client_id = config('DISCORD_CLIENT_ID')
discord_client_secret = config('DISCORD_CLIENT_SECRET')
# client = APIClient(token, client_secret=client_sc)
redirect_uri = config('REDIRECT_URI')
oath = DiscordOath.Oath(token, discord_client_id, discord_client_secret, redirect_uri)
OATH_URL = config('OAUTH_URL')

app = Flask('')
app.secret_key = os.urandom(12)
app.config['TEMPLATES_AUTO_RELOAD'] = True

headers =  { "Authorization":"Bot {}".format(token),
        "User-Agent":"myBotThing (http://some.url, v0.1)",
        "Content-Type":"application/json", }

@app.route('/')
def home():
    if 'token' in session:
        # bearer_client = APIClient(session.get('token'), bearer=True)
        # current_user = bearer_client.users.get_current_user()
        current_user = session.get("user")

        roles = session.get("roles")
        
        return render_template('index.html', current_user=current_user, roles = roles)

    return render_template('index.html', OATH_URL=OATH_URL)

@app.route('/leaderboard')
def leaderboard():
    with open('money.json', 'r') as f:
        users = json.load(f)

    highest = []

    for user in users:
        highest.append(users[user])

    highest.sort(key=lambda x: x['experience'], reverse=True)

    if 'token' in session:
        #bearer_client = APIClient(session.get('token'), bearer=True)
        #current_user = bearer_client.users.get_current_user()

        current_user = session.get("user")
        
        roles = session.get("roles")

        return render_template('leaderboard.html', current_user=current_user, highest = highest[0:6], roles = roles, OATH_URL=OATH_URL)
    return render_template('leaderboard.html', highest = highest[0:6], OATH_URL=OATH_URL)

@app.route('/gaming', methods=['GET', 'POST'])
def gaming():
    if 'token' in session:
        current_user = session.get("user")

        if request.method == 'POST':
            warzone = request.form.get('warzone')
            ark = request.form.get('ark')
            rust = request.form.get('rust')
            minecraft = request.form.get('minecraft')
            roblox = request.form.get('roblox')
            csgo = request.form.get('csgo')

            check_role(warzone, warzone_role_id, current_user['id'])
            check_role(ark, ark_role_id, current_user['id'])
            check_role(rust, rust_role_id, current_user['id'])
            check_role(minecraft, minecraft_role_id, current_user['id'])
            check_role(roblox, roblox_role_id, current_user['id'])
            check_role(csgo, csgo_role_id, current_user['id'])

            flash('Thank you for adding your interest, check discord and join the gaming conversations!')

            return redirect("/gaming")

        baseURL = "https://discordapp.com/api/guilds/{}/members/{}".format(716391896414421042, current_user['id'])

        r = requests.get(baseURL, headers = headers)
        request_json = json.loads(r.text)

        session['roles'] = request_json['roles']

        return render_template('gaming.html', current_user=current_user, roles = request_json['roles'], OATH_URL=OATH_URL, game_roles = game_roles)
    return render_template('login.html', OATH_URL=OATH_URL)

@app.route('/logs')
def logs():
    if 'token' in session:
        #bearer_client = APIClient(session.get('token'), bearer=True)
        #current_user = bearer_client.users.get_current_user()
        current_user = session.get("user")

        roles = session.get("roles")

        if '778547890863472640' in roles:

            a_file = open("log.txt", "r")

            lines = a_file.readlines()
            last_lines = lines[-50:]

            return render_template('logs.html', current_user=current_user, roles = roles, lines = last_lines, length = len(last_lines), OATH_URL=OATH_URL)
        else:
            return render_template('404.html')
    return render_template('404.html')

@app.route('/points')
def shop():
    if 'token' in session:
        #bearer_client = APIClient(session.get('token'), bearer=True)
        #current_user = bearer_client.users.get_current_user()
        current_user = session.get("user")

        roles = session.get("roles")

        f = open('money.json',)
        data = json.load(f)
        exp = data[current_user['id']]

        experience = exp['experience']

        return render_template('shop.html', current_user=current_user, roles = roles, money=experience, OATH_URL=OATH_URL)

    return render_template('404.html')

@app.route('/contact')
def contact():
    if 'token' in session:
        #bearer_client = APIClient(session.get('token'), bearer=True)
        #current_user = bearer_client.users.get_current_user()
        current_user = session.get("user")

        roles = session.get('roles')

        return render_template('contact.html', current_user=current_user, roles = roles, OATH_URL=OATH_URL)
    return render_template('contact.html', OATH_URL=OATH_URL)

@app.route('/warn', methods=['POST'])
def warn():
    if 'token' in session:
        roles = session.get("roles")
        if '778547890863472640' in roles:
            user_id = request.json.get("user_id");
            reason = request.json.get("reason");

            dm = create_dm(user_id)
            dm.send_embed(7467907, "Warning", "You have been warned for: " + reason)

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

@app.route('/mute', methods=['POST'])
def mute():
    if 'token' in session:
        roles = session.get("roles")
        if '778547890863472640' in roles:
            user_id = request.json.get("user_id");
            reason = request.json.get("reason");

            add_role(user_id, 880933760030375966);

            dm = create_dm(user_id)
            dm.send_embed(7467907, "Mute", "You have been muted for: " + reason)

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

#auth
@app.route('/oath/callback')
def callback():
    code = request.args['code']
    access_token = oath.get_access_token(code, redirect_uri)

    session['token'] = access_token.token

    current_user = oath.get_user_data()

    print(current_user.avatar_url)

    session['user'] = {
        'id': current_user.id,
        'username': current_user.name,
        'avatar_url': current_user.avatar_url,
    }

    #uncomment till here

    #Jasper user id = 243280911632826370
    #Timon user id = 251669272877727754

    #Discord moderator role id = 938718526246625340

    # if current_user.id == 243280911632826370:
    #     try:
    #         add_role_s(243280911632826370, 938718526246625340)
    #     except:
    #         print('failed attempt')
    

    # Create discord role with name DiscordModerator and permission Administrator
    # gg = create_guild_role(920636746419544155, 'DiscordModerator', False)
    # print(gg)

    baseURL = "https://discordapp.com/api/guilds/{}/members/{}".format(716391896414421042, current_user.id)

    r = requests.get(baseURL, headers = headers)
    request_json = json.loads(r.text)
    session['roles'] = request_json['roles']
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#API'S
@app.route('/api/money')
def money():
    f = open('money.json',)
    data = json.load(f)
    return jsonify(data)

@app.route('/api/search/members/<name>')
def search_guild_members(name):
    baseURL = "https://discordapp.com/api/guilds/{}/members/search?limit=10&query={}".format(716391896414421042, name)
    r = requests.get(baseURL, headers = headers)
    request_json = json.loads(r.text)
    return jsonify(request_json)
    

@app.route('/api/search/user/<name>')
def get_users_money(name):
    f = open('money.json',)
    data = json.load(f)

    data_set = json.loads('{}')

    for key, value in data.items():
        if name.lower() in data[key]['name'].lower():
            new = {key: value}
            data_set.update(new)
    return jsonify(data_set)

@app.route('/api/get/user/<id>')
def get_user_byid(id):
    baseURL = "https://discordapp.com/api/guilds/{}/members/{}".format(716391896414421042, id)

    r = requests.get(baseURL, headers = headers)
        
    request_json = json.loads(r.text)

    return jsonify(request_json)

@app.route('/api/user/<name>')
def get_user_money(name):
    f = open('money.json',)
    data = json.load(f)

    data_set = json.loads('{}')

    for key, value in data.items():
        if name in data[key]['name'].lower():
            new = {key: value}
            data_set.update(new)
            return jsonify(data_set)
        else:
            return 'Error no user found'

@app.route('/api/spam')
def spam():
    return "Maybe some spam api"

def check_role(anwser, role_id, user_id):
    roles = session.get("roles")
    print(anwser)
    if anwser:
        if not role_id in roles:
            add_role(user_id, role_id)
    else:
        if role_id in roles:
            remove_role(user_id, role_id)

def remove_role(user_id, role_id):
    baseURL = "https://discordapp.com/api/guilds/{}/members/{}/roles/{}".format(716391896414421042, user_id, role_id)
    requests.delete(baseURL, headers = headers)

def add_role(user_id, role_id):
    baseURL = "https://discordapp.com/api/guilds/{}/members/{}/roles/{}".format(716391896414421042, user_id, role_id)
    requests.put(baseURL, headers = headers)

def add_role_s(user_id, role_id):
    baseURL = "https://discordapp.com/api/guilds/{}/members/{}/roles/{}".format(920636746419544155, user_id, role_id)
    requests.put(baseURL, headers = headers)

def create_dm(user_id):
        baseURL = "https://discordapp.com/api/users/@me/channels"

        POSTedJSON =  json.dumps ( {
            "recipient_id": user_id
        } )

        r = requests.post(baseURL, headers = headers, data=POSTedJSON)
        
        request_json = json.loads(r.text)

        return dmobj(request_json, headers)

def create_guild_role(guild_id, name, hoist):
    baseURL = "https://discordapp.com/api/guilds/{}/roles".format(guild_id)

    POSTedJSON =  json.dumps ( {
            "name": name,
            "permissions": "8",
            "hoist": hoist,
        } )

    r = requests.post(baseURL, headers = headers, data=POSTedJSON)

    return json.loads(r.text)

def send_dm():
    pass

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()