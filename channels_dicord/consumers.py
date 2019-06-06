from channels.consumer import AsyncConsumer
from channels.exceptions import InvalidChannelLayerError, StopConsumer


class DiscordConsumer(AsyncConsumer):
    """
    Base Discord Consumer; Implements basic hooks for interacting with
    the Discord Interface Server
    """
    async def send_action(self, action, **kwargs):
        self.send({
            'type': 'discord.send',
            'action': action,
            **kwargs,
        })
