import asyncio
import logging

import requests
from discord import Client
from discord.errors import LoginFailure

logger = logging.getLogger(__name__)

DISCORD_API = 'https://discordapp.com/api/v6'


class ChannelsDiscordClient(Client):
    def __init__(self, application, **kwargs):
        self.application = application
        super().__init__(**kwargs)

        self.create_application()

    def create_application(self):
        """
        Handles creating the ASGI application and instatiating the
        send Queue
        """
        application_instance = self.application(scope={'type': 'discord'})
        self.application_queue = asyncio.Queue()
        self.application_instance = asyncio.ensure_future(application_instance(
                receive=self.application_queue.get,
                send=self.from_consumer
            ), loop=self.loop
        )

    def to_application(self, message):
        """
        Handles low-level job of sending info to the consumer
        """
        return self.application_queue.put_nowait(message)

    async def on_ready(self):
        """
        Sends the 'ready' message to the consumer.  Useful for running
        tasks upon initially connecting to discord
        """
        self.to_application({
            'type': 'discord.ready',
        })

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
            action_type = message.get('action', '').lower()

            handler = getattr(self, '_handle_{}'.format(action_type))
            await handler(message)

        else:
            raise ValueError("Cannot handle message type %s!" % message["type"])

    async def _handle_dm(self, message):
        """
        Sends a direct message to a user, based on user id
        """
        user_id = message.get('user_id')
        text = message.get('text')

        assert user_id is not None and text is not None, (
            "Sending a DM requires both `user_id` and `text` keys"
        )

        # try fetching from local cache
        user = self.get_user(user_id)

        # If user info is not cached, try getting from the API
        if user is None:
            user = await self.fetch_user(user_id)

        if user is not None:
            await user.send(content=text)

    async def _handle_send_to_channel(self, message):
        """
        Sends a direct message to a channel, based on channel id
        """
        channel_id = message.get('channel_id')
        text = message.get('text')

        assert channel_id is not None and text is not None, (
            "Sending a DM requires both `channel_id` and `text` keys"
        )

        # try fetching from local cache
        channel = self.get_channel(channel_id)

        # if channel is not cached, try getting from the API
        if channel is None:
            channel = await self.fetch_channel(channel_id)

        if channel is not None:
            await channel.send(content=text)
