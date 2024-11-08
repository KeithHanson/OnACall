# Cheap Yellow Display + Discord Selfbot = OnACallBot

The goal of this bot is to watch your own discord messages and broadcast important ones over UDP.

Another device/program/etc should be listening on the UDP port 13337 to react to these incoming messages.

Once the Microcontroller code is built (soon), this will allow a simple screen to show you the last VIP messages, or easily show people around you irl that you are not talking to them, you are on a call.

## Installation

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Operation

Edit your .env (see `.env-sample`), and follow the directions here for getting your token:

https://discordpy-self.readthedocs.io/en/latest/authenticating.html#how-do-i-obtain-mine

`python bot.py` to begin running the bot.

Important message will now be sent out on a UDP broadcast packet. 

As a quick test, you can use netcat to view the packets:

`nc -l -u -p 13337 -k`
