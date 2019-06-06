import asyncio

import requests
from discord import Client
from discord.errors import LoginFailure


DISCORD_API = 'https://discordapp.com/api/v6'

DISCORD_PERMISSIONS = 0x800


class ChannelsDiscordClient(Client):
    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.application = application
        self.create_application()

    def noop_from_consumer(self, msg):
        """
        empty default for receiving from consumer
        """

    def create_application(self):
        """
        Handles creating the ASGI application and instatiating the
        send Queue
        """
        application_instance = self.application(scope={'type': 'discord'})
        self.application_queue = asyncio.Queue()
        self.application_instance = asyncio.ensure_future(application_instance(
            receive=self.application_queue.get,
            send=from_consumer),
            loop=self.loop
        )

    async def from_consumer(self, message):
        """
        Receives message from channels from the consumer.  Message should have the format:
            {
                'type': 'discord.send',
                'action': VALID_ACTION_TYPE
            }
        """
        if "type" not in message:
            raise ValueError("Message has no type defined")

        elif message['type'] == 'discord.send':
            command_type = message.get('action', '').lower()

            handler = getattr(self, '_handle_{}'.format(command_type))
            await handler(message)

        else:
            raise ValueError("Cannot handle message type %s!" % message["type"])

    async def handle_dm(self, message):
        """
        Sends a direct message to a user, based on user id
        """
        user_id = message.get('user_id')
        text = message.get('text')

        assert user_id is not None and text is not None, (
            "Sending a DM requires both `user_id` and `text` keys
        )

        user = self.get_user(user_id)

        if user is not None:
            await user.send(content=text)
