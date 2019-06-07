from channels.consumer import AsyncConsumer
from channels.exceptions import InvalidChannelLayerError, StopConsumer


class DiscordConsumer(AsyncConsumer):
    """
    Base Discord Consumer; Implements basic hooks for interacting with
    the Discord Interface Server
    """
    async def send_action(self, action, **kwargs):
        await self.send({
            'type': 'discord.send',
            'action': action,
            **kwargs,
        })

    async def discord_ready(self, event):
        """
        Runs when initially connected to discord.  This method is primarily
        used for internal tasks, such as adding groups to the channel layer.
        Any tasks meant to be run on initially connecting should be called
        by overriding the `ready` method in your app's consumer
        """
        try:
            for group in self.groups:
                await self.channel_layer.group_add(group, self.channel_name)
        except AttributeError:
            raise InvalidChannelLayerError("BACKEND is unconfigured or doesn't support groups")
        await self.ready()

    async def ready(self):
        """
        Hook for any action(s) to be run on connecting to Discord server
        """
        pass
