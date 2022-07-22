from discord import Discord
import os
import json
import random
import threading
import praw
import time

import math

import datetime

from keep_alive import keep_alive
from decouple import config

#USE kill 1 in shell

# token = os.environ['DISCORD_BOT_SECRET']
token = config('DISCORD_BOT_SECRET')
discord_client_id = config('DISCORD_CLIENT_ID')
discord_client_secret = config('DISCORD_CLIENT_SECRET')
users_msg_time = {}
client = Discord.Client()

# reddit = praw.Reddit(client_id=os.environ['REDDIT_ID'],
#     client_secret=os.environ['REDDIT_SECRET'],
#     user_agent="discordBot")

reddit = praw.Reddit(client_id=config('REDDIT_ID'),
    client_secret=config('REDDIT_SECRET'),
    user_agent="discordBot")

@client.event()
def on_ready():
    print('Logged in!')
    for guild in client.get_guilds():
        role = client.get_role(guild['id'], "member")
        if role:
            for member in client.get_guild_members(guild['id']):
                if not member.has_role(role.id):
                    print('Adding role to: {}'.format(member.name))
                    member.add_role(guild['id'], role.id)

@client.command(alias=['smiley'])
def smile(ctx):
    ctx.add_reaction("\N{SLIGHTLY SMILING FACE}")

@client.command(alias=['greeting', 'greet'])
def hello(ctx):
    ctx.reply("Greetings!")

@client.command(alias=['downloads', 'install'])
def download(ctx):
    client.sendEmbed(
            ctx.channel_id, 7467907, "Download:",
            "[Download addon here](https://jaspervdijk63.github.io/downloads.html)")

@client.command(alias=['videos', 'videohelp'])
def video(ctx):
    client.sendEmbed(
            ctx.channel_id, 1759423, "Video help",
            'How to use the addon: \n https://youtu.be/YsGRvSJMe_4 \nAddon installation video to world: \n https://youtu.be/4olxWWwaLLQ'
        )

@client.command(alias=['cointoss', 'flipcoin'])
def coinflip(ctx):
    flipper = [
            'head', 'tail', 'head', 'tail', 'head', 'tail', 'head', 'tail',
                    'head', 'tail'
        ]
    ctx.reply(f'{ctx.mention_author} ' + random.choice(flipper))

@client.command(alias=['helpme'])
def help(ctx):
    client.sendEmbed(
    ctx.channel_id, 1759423, "Commands help",
    "!hello - Sends greetings. \n\n !smile - Replies with a smiley \n\n !download - Sends download link \n\n !video - Sends video help \n\n !coinflip - flips the coin! \n\n !help - Shows this message! \n\n !meme - Sends a meme! \n\n !nsfw - Sends a nsfw pic \n\n !fight - Fight a mentioned player NOT AVAILABLE CURRENTLY \n\n !remove - Remove specified amount of messages \n\n !level - Shows your current level! \n\n !leaderboard - Shows the server leaderboard for levels! \n\n !rules - Shows the server rules!")

@client.command(alias=['purge', 'prune', 'delete'])
def remove(ctx):
    if '778547890863472640' in ctx.author_roles:
                total = int(ctx.args[0])
                ctx.delete_message()
                client.delete_messages(760788145658265600, total)
    else:
        ctx.reply("You don't have the right permissions!")

@client.command(alias=['leader', 'board'])
def leaderboard(ctx):
    with open('money.json', 'r') as f:
        users = json.load(f)

        f.close()

    highest = []

    for user in users:
        highest.append(users[user])

        msg = ""

        highest.sort(key=lambda x: x['experience'], reverse=True)

        i = 1
        for usr in highest:
            msg += '\n\n {}. **{}** at level: {}'.format(i, usr['name'], usr['level'])
            i+=1
            if i >= 6:
                break

    ctx.reply_embed(1759423, '', msg)

@client.command(alias=['memes', 'reddit'])
def meme(ctx):
    imageUrls = []
    titles = []
    for submission in reddit.subreddit("memes").hot(limit=40):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            imageUrls.append(submission.url)
            titles.append(submission.title)
    random_post_number = random.randint(0, len(imageUrls))
    for i,image in enumerate(imageUrls):
        if i==random_post_number:
            ctx.reply_embed(1759423, titles[i], "", "", "", image)

@client.command(alias=['porn', 'nude', 'nudes'])
def nsfw(ctx):
    if ctx.channel.is_nsfw:
        imageUrls = []
        titles = []
        for submission in reddit.subreddit("nsfw").hot(limit=40):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                imageUrls.append(submission.url)
                titles.append(submission.title)
        random_post_number = random.randint(0, len(imageUrls))
        for i,image in enumerate(imageUrls):
            if i==random_post_number:
                ctx.reply_embed(1759423, titles[i], "", "", "", image)
    else:
        ctx.reply("Get your ass to a nsfw channel!")

@client.command(alias=['rule'])
def rules(ctx):
    client.sendEmbed(
        ctx.channel_id, 1759423, "Server rules",
        '''1. No spamming - this includes mass mentions, mentioning with no reason, chat flooding or other associated activities
        \n2. Self promotion outside of the designated channels is not permitted.
        \n3. Strictly no NSFW content outside of the NSFW designated channel. This includes text, images, videos and links that contain it. We have a zero-tolerance policy for this
        \n4. Treat everyone with respect. Any discrimination for any reason will not be permitted. Note that this includes discussing topics that may provoke an extreme reaction or hurt others emotionally, mentally or physically isn't allowed
        \n5. Excessive swearing or the use of offensive language such as racial slurs is not permitted
        \n6. Don't engage in arguments. This includes arguing with a staff member. If you have a complaint about a staff member, DM an available admin or owner
        \n6. Don't beg or ask for things such as roles or nitro. You won't get it and it's just annoying
        \n7. Don't engage in conversations involving illegal or offensive topics
        \n8. Please speak English, it's allows the most efficient moderation
        \n9. Don't troll or annoy people, or exploit any loopholes you may find
        \n10. Use channels for the correct reason, and respect staff if they ask you to move a channel
        \n11. No inappropriate usernames, custom status' or profile pictures
        \n12. Don't use alts in malicious ways
        \n13. DO NOT spam ping anyone (including moderators).''')

@client.command(alias=['admin', 'adminpanel'])
def panel(ctx):
    if '772900568624660570' == ctx.channel_id:
        if '778547890863472640' in ctx.author_roles:
            client.sendEmbed(
                ctx.channel_id, 1759423, "Web panel", "https://DCBotAPI.hr3edits.repl.co")
        else:
            ctx.reply("You don't have the right permissions!")
    else:
        ctx.reply("This command can only be used in the staff chat!")

@client.event()
def on_message(ctx):
    if '880933760030375966' in ctx.author_roles:
        ctx.del_msg()
        return

    anti_spam(ctx)

    if ctx.command == "!level":
        with open('money.json', 'r') as f:
            users = json.load(f)

            f.close()
        user = ctx.author_id
        level = users[f'{user}']['level']
        #ctx.delete_message()
        ctx.reply_embed(1759423, '', f'Your level is: **{level}**') 

    hanle_level_system(ctx)


@client.event()
def on_member_join(member):
    with open('lines.txt') as json_file:
        data = json.load(json_file)

        json_file.close()

    text = data[random.randint(0, len(data))]

    client.sendEmbed(716394570220437555, 1759423,
                     "Welcome", text.format(member.mention))

@client.event()
def on_reaction(reaction):
    if reaction.emoji == "👍" and reaction.message_id == "841444725278113832":
        client.add_role(reaction.guild_id, reaction.user_id,
                        716396660271611984)
        client.delete_reaction(reaction.channel_id, reaction.message_id, "??",
                               reaction.user_id)


@client.event()
def on_log(ctx):
    if not ctx.content == "":
        print('Log: {0.author_username} said {0.content}'.format(ctx))
        with open("log.txt", "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            file_object.write('{} said {} at {}'.format(ctx.author_username, ctx.content, current_time))
        file_object.close()


def hanle_level_system(ctx):
    with open('money.json', 'r') as f:
        users = json.load(f)

        f.close()

    x = threading.Thread(target=update_data,
                         args=(users, ctx.author_id, ctx.author_username,
                               ctx.mention_author))
    x.start()

# Update level en exp


def update_data(users, user_id, user_name, user_mention):
    if not f'{user_id}' in users:
        users[f'{user_id}'] = {}
        users[f'{user_id}']['experience'] = 0
        users[f'{user_id}']['level'] = 1
        users[f'{user_id}']['name'] = user_name
        users[f'{user_id}']['time'] = time.time()

        with open('money.json', 'w') as f:
            json.dump(users, f)
        f.close()

        x = threading.Thread(target=add_experience,
                             args=(user_id, 20, user_name, user_mention))
        x.start()
    else:
        x = threading.Thread(target=add_experience,
                             args=(user_id, 20, user_name, user_mention))
        x.start()

# Add EXP


def add_experience(user_id, exp, user_name, user_mention):
    with open('money.json', 'r') as f:
        users = json.load(f)
    f.close()

    if time.time() - users[f'{user_id}']['time'] >= 20:
        users[f'{user_id}']['experience'] += exp
        users[f'{user_id}']['time'] = time.time()
        users[f'{user_id}']['name'] = user_name

        with open('money.json', 'w') as f:
            json.dump(users, f)
        f.close()

    
    users[f'{user_id}']['name'] = user_name

    x = threading.Thread(target=level_up,
                         args=(user_id, user_name, user_mention))
    x.start()

# Level UP
def level_up(user_id, user_name, user_mention):
    with open('money.json', 'r') as f:
        users = json.load(f)
    f.close()

    experience = users[f'{user_id}']['experience']
    lvl_start = users[f'{user_id}']['level']
    users[f'{user_id}']['name'] = user_name
    #lvl_end = int(experience**(1 / 4))
    lvl_end = int(.25 * math.sqrt(experience))
    print(lvl_start)
    print(lvl_end)
    if lvl_end > lvl_start:
        print('------------')
        print(lvl_start)
        print(lvl_end)
        users[f'{user_id}']['level'] = lvl_end
        with open('money.json', 'w') as f:
            json.dump(users, f)
        f.close()

        client.create_dm(user_id).send_embed(7467907, "New level:", f'{user_mention} has reached level **{lvl_end}**!')
    else:
        with open('money.json', 'w') as f:
            json.dump(users, f)

            f.close()


def anti_spam(ctx):
    with open('spam.json', 'r') as f:
        users = json.load(f)

        f.close()

    user_id = ctx.author_id
    user_name = ctx.author_username
    
    if not f'{user_id}' in users:
        users[f'{user_id}'] = {}
        users[f'{user_id}']['name'] = user_name
        users[f'{user_id}']['time'] = time.time()

        note = {}
        note['message'] = ctx.content
        note['time'] = time.time()
        note['channel_id'] = ctx.channel_id
        note['message_id'] = ctx.message_id
        
        users[f'{user_id}']['messages'] = []
        users[f'{user_id}']['messages'].append(note)

        with open('spam.json', 'w') as f:
            json.dump(users, f)

        f.close()

    else:
        broken = False
        if len(users[f'{user_id}']['messages']) >= 3:
            for x in users[f'{user_id}']['messages']:
                if ctx.content != x['message'] or time.time() - x['time'] >= 30 or ctx.content == "" or ctx.content == "!meme" or ctx.content == "!nsfw" or ctx.content == "!coinflip":
                    broken = True
        else:
            broken = True

        if not broken:
            role = client.get_role(ctx.guild_id, "Mute")
            client.add_role(ctx.guild_id, ctx.author_id, role.id)
            text = "{} ( current name: {} ) has been muted for spamming: {}"
            client.sendEmbed(772900568624660570, 1759423,
                     "Muted", text.format(ctx.mention_author, ctx.author_username, ctx.content))

            client.create_dm(ctx.author_id).send_embed(7467907, "You have been muted:", f'You have been muted for spamming. If you believe this is a issue send a message to a staff member so they can resolve this.')

            for x in users[f'{user_id}']['messages']:
                client.delete_message(x['channel_id'], x['message_id'])

            ctx.delete_message()

        if len(users[f'{user_id}']['messages']) >= 3:
            users[f'{user_id}']['messages'].pop(0)

        note = {}
        note['message'] = ctx.content
        note['time'] = time.time()
        note['channel_id'] = ctx.channel_id
        note['message_id'] = ctx.message_id

        users[f'{user_id}']['messages'].append(note)

        with open('spam.json', 'w') as f:
            json.dump(users, f)

        f.close()

if __name__ == "__main__":
    # Start bot
    keep_alive()
    client.start(token, '!')