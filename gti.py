import discord
import asyncio

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


    if message.content.startswith('!channels'):
    #This is used to debug channel tagging on a private server
        verify = message.channel.server.get_channel('445317164891766814')
        rules = message.channel.server.get_channel('360823809286340608')
        tmp = '{0.mention},{1.mention}'
        await client.send_message(server, tmp.format(verify,rules))
        print(message.content + " was replied to with " + tmp)




@client.event
async def on_member_join(member):
    #This is used to greet a user in the #general channel of Official GTI Discord
    server = member.server.get_channel('368049600885686278')
    verify = member.server.get_channel('368081743795978243')
    rules = member.server.get_channel('368081632776683531')

    fmt = 'Welcome {0.mention}! If you would like a role, head over to {1.mention} and post a picture of your ride! ' \
          'Be sure to check out [2.mention] as well, and ,importantly, make sure to have fun!'
    await client.send_message(server, fmt.format(member,verify,rules))


client.run(Token)
