import discord

import htwk_logging

TOKEN_FILE = "token"
LOG = htwk_logging.create_logger(__name__)


class Handle:

    def __init__(self):
        pass

    command = None

    def on_message(self, bot: "Bot", client, message, raw_message):
        """
        Method that is called when the command specified by the handle is received
        :param bot: instance of the bot, of class Bot
        :param client: client instance of the bot, of class discord.Client
        :param message: argument string of the received message, not including the command, of class str
        :param raw_message: full message with related members such as author, of class discord.Message
        :return: nothing
        """
        pass

    def man(self):
        pass


client = discord.Client()


class Bot:
    Instance = None
    token = None

    @staticmethod
    def get():
        if Bot.Instance is None:
            Bot.Instance = Bot()
        return Bot.Instance

    def __init__(self):
        with open(TOKEN_FILE, "r") as token_file:
            self.token = token_file.readline()
        self.handles = list()
        self.msg_buffer = list()
        self.msg_tts_buffer = list()

    def start(self):
        client.run(self.token)

    def add_handle(self, handle):
        self.handles.append(handle)

    def send_message(self, msg):
        self.msg_buffer.append(msg)

    def send_message_tts(self, msg):
        self.msg_tts_buffer.append(msg)


@client.event
async def on_message(message):
    # dont reply to itself
    if message.author == client.user:
        return

    LOG.info("got new message: [%s] %s", message.author, message.content)
    msg_arr = message.content.split()

    if len(msg_arr) != 0 and msg_arr[0][0] is "!":

        msg_command = msg_arr[0][1:len(msg_arr[0])]

        for handle in Bot.get().handles:
            try:
                if handle.command == msg_command:
                    handle.on_message(Bot.get(), client, " ".join(msg_arr[1:len(msg_arr)]), message)
            except Exception as e:
                await client.send_message(message.channel, str(e))

    # SEND ALL PENDING MESSAGES TO THE SERVER
    for msg in Bot.get().msg_buffer:
        if isinstance(msg, str) and len(msg) > 0:
            await client.send_message(message.channel, msg)
    Bot.get().msg_buffer.clear()

    # SEND ALL PENDING TTS MESSAGES TO THE SERVER
    for msg in Bot.get().msg_tts_buffer:
        if isinstance(msg, str) and len(msg) > 0:
            await client.send_message(message.channel, msg, tts = True)
    Bot.get().msg_tts_buffer.clear()


@client.event
async def on_ready():
    LOG.info("user " + client.user.name + " with id " + str(client.user.id) + " logged in")
