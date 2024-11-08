import json
import discord
from dotenv import load_dotenv
import os
import socket

if not os.path.exists('.env'):
    print("YOU MUST PROVIDE A .env FILE HERE. Sample:")
    help_text = """
DISCORD_SELFBOT_TOKEN="MTAyM...."
VIPS="username1,username2,username3"
CYD_PAIR_KEY="1234"
"""
    print(help_text)
    print("See here to get your selfbot token: https://discordpy-self.readthedocs.io/en/latest/authenticating.html#how-do-i-obtain-mine")

load_dotenv()

udp_socket = None
broadcast_address = ('<broadcast>', 13337)
vips = []

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        for vip in vips:
            if vip in str(message.author):
                print("\nVIP MESSAGE ALERT! About to UDP broadcast payload:")

                # these will be sent out as UDP broadcast - the pair_key will allow the 
                # CYD to ignore everything but the paired bot if multiple bots are running on the same network.

                payload = json.dumps({
                    "channel": str(message.channel),
                    "author": message.author.display_name, 
                    "message": message.clean_content, 
                    "author_avatar": message.author.display_avatar.url,
                    "pair_key": os.getenv("CYD_PAIR_KEY") 
                }) + "\n"

                print(payload)

                udp_socket.sendto(payload.encode(), broadcast_address)
        
        if str(message.channel).startswith("Direct Message"): 
            print(f'Direct Message from FROM {message.author}:\n{message.clean_content}\n')

    async def on_call_create(self, call):
        print("ON A CALL!")
        print(call)

    async def on_call_delete(self, call):
        print("OFF THE CALL!")
        print(call)

client = MyClient()

if not os.getenv("DISCORD_SELFBOT_TOKEN") or not os.getenv("DISCORD_SELFBOT_TOKEN").strip():
    print("PLEASE SET THE ENV VAR DISCORD_SELFBOT_TOKEN\nhttps://discordpy-self.readthedocs.io/en/latest/authenticating.html")

elif not os.getenv("CYD_PAIR_KEY"): 
    print("PLEASE PROVIDE A CYD_PAIR_KEY='123456' in .env!")

elif not os.getenv("VIPS") or not os.getenv("VIPS").strip():
    print("PLEASE PROVIDE A VIPS='username,username2' in .env!")

else:
    vips = os.getenv("VIPS").split(",")
    print("Loaded VIPS:")
    print(vips)

    print("Opening UDP broadcast socket.")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.run(os.getenv("DISCORD_SELFBOT_TOKEN"))
