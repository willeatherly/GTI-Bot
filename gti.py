import discord
import asyncio
import requests
from io import open as iopen
import time
import os
import base64
import json
import re

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    server = message.channel
    if message.content.startswith('!test'):
    #This is used to debug user tagging on a private server.
        tmp = '{0.author.mention} is pretty cool'.format(message)
        await client.send_message(server, tmp)
        print(message.content +" was replied to with " + tmp)

    if message.content.startswith("yeet") or message.content.startswith("Yeet") or message.content.startswith("YEET"):

        await ctx.send_message(server,"<:yeet:527886013381476352>")

        print(message.content + " was made by " + '{0.author}')

    #This is used to interact with the CV API
    if message.content.startswith("!v"):

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key='

        try:
            print(message.attachments)
            preimg = re.search(r"([^-]+)-([^-]+)",str(message.attachments))
            img = preimg.group()
            print(img)
            name = requests_image(img)

            with open(name,'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())

            r = requests.post(url,data=img_base64)

            jfile = r.json()

            mm = jfile['results'][0]['vehicle']['make_model'][0]['name'].split("_")
            year = jfile['results'][0]['vehicle']['year'][0]['name'].split("-")

            print(mm)
            print(year)

            if mm[0] == 'volkswagen':

                if mm[1] == 'golf' or mm[1] == 'gti' or mm[1] == 'golf-gti':

                    if year [0] == '1980' or year[0] == '1975':
                        role = discord.utils.get(message.channel.server.roles, name="Mk1")
                        user = message.author
                        await user.add_roles(role)

                    if year [0] == '1985' or year[0] == '1990':
                        role = discord.utils.get(message.channel.server.roles, name="Mk2")
                        user = message.author
                        await user.add_roles(role)

                    if year[0] == '1995':
                        role = discord.utils.get(message.channel.server.roles, name="Mk3")
                        user = message.author
                        await user.add_roles(role)

                    if year[0] == '2000':
                        role = discord.utils.get(message.channel.server.roles, name="Mk4")
                        user = message.author
                        await user.add_roles(role)

                    if year[0] == '2005':
                        role = discord.utils.get(message.channel.server.roles, name="Mk5")
                        user = message.author
                        await user.add_roles(role)

                    if year[0] == '2010':
                        role = discord.utils.get(message.channel.server.roles, name="Mk6")
                        user = message.author
                        await user.add_roles(role)

                    if year[0] == '2015':
                        role = discord.utils.get(message.channel.server.roles, name="Mk7")
                        user = message.author
                        await user.add_roles(role)

                else:
                    role = discord.utils.get(message.channel.server.roles, name="Other Volks")
                    user = message.author
                    await user.add_roles(role)

            else:
                role = discord.utils.get(message.channel.server.roles, name="Other Volks")
                user = message.author
                await user.add_roles(role)





            os.remove(name)
        except IndexError:
            print("we messed up, try again")


def requests_image(file_url):

    file_name = "verfy" + str(time.time()) + ".jpg"
    i = requests.get(file_url)
    if i.status_code == requests.codes.ok:
        with iopen(file_name, 'wb') as file:
            file.write(i.content)

    else:
        return False

    return file_name



    #server = message.channel.server.get_channel('549409632985153556')
    #async for log in client.logs_from(message.channel, limit=300):
    #    length = len(log.reactions)
    #    if length > 0:
    #        if length == 3:
    #            #await client.add_reaction(log, "<:yeet:527886013381476352>")
    #            await client.send_message(server, '{0.mention} sent:'.format(log.author))
    #            await client.send_message(server, log.content)


@client.event
async def on_reaction_add(reaction,user):
    #this handles top posts
    server = reaction.message.channel.server.get_channel('550204923103543297')
    count = 0
    banned = False
    #goes through all message reactions
    for react in reaction.message.reactions:
        #checks for emoji
        if str(react.emoji) == '<:BW:478397214323113995>':
            count = count +1
            #threshold, edit this if you want to increase or decrease
            if count == 7:
                #checks for repeats of the same message. keeps it original. I am still working on this bit
                async for log in client.logs_from(server, limit=300):

                    #breaks when it finds a similar message
                    if str(log.content) == str(reaction.message.content):
                        print("denied")
                        banned = True
                        break

                if banned:
                   break
                else:
                #posts if requirements are met
                    print("posting another message")
                    await client.send_message(server, '{0.mention} sent:'.format(reaction.message.author))
                    await client.send_message(server, reaction.message.content)


@client.event
async def on_member_update(before,after):
   #booleans to test the serarch
    bef = True
    af = False
    #checking the precondition
    for rollie in before.roles:
        if rollie.id == '543460962745843712':
            bef = False
    #checking the post condition
    for role in after.roles:

        if role.id == '543460962745843712':

            af = True
    #If the role is changed, launch the message
    if bef == True and af == True:
        tmp = '{0.mention}, welcome to Time Out. You have been placed here by a member of the server staff due to misconduct on the server. ' \
              'You are currently muted in every channel except for this one. If you have any questions about your predicament, feel free to contact' \
              ' a member of the server staff.'.format(after)

        await client.send_message(after.server.get_channel('550166898441060352'), tmp)




@client.event
async def on_member_join(member):
    #This is used to greet a user in the #general channel of Official GTI Discord
    server = member.server.get_channel('368049600885686278')
    verify = member.server.get_channel('368081743795978243')
    rules = member.server.get_channel('368081632776683531')

    fmt = 'Welcome {0.mention}! If you would like a role, head over to {1.mention} and post a picture of your ride! ' \
          'Be sure to check out {2.mention} as well, and ,importantly, make sure to have fun!'
    await client.send_message(server, fmt.format(member,verify,rules))



client.run(Token)
