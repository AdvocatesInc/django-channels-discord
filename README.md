# Channels-Discord

**Django Channels Discord** is a bridge between Discord (currently using the [pycord](https://github.com/Pycord-Development/pycord) Python library, but this may be a stopgap while we wait for the dust to settle after discord.py's [implosion](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1)) and Django's [channels](https://github.com/django/channels)).  It contains both a new interface server for connecting to Discord and Channels consumers -- everything you need to turn your Django app into an Discord chatbot, chat monitoring/moderating service, or whatever else you might use a real-time Discord client to do.

This project is more of a stub right now, and will be more further fleshed out as new features are wired up from discord.py.

## Requirements

Most of the requirements can be found in setup.py, but the most important note is that this requires library requires [Django Channels 3+](https://channels.readthedocs.io/en/latest/) -- Channels 1.x and 2.x are not supported.

## Installation

Install the package from github:

```bash
pip install git+https://github.com/AdvocatesInc/django-channels-discord.git@0.1
```

## Basic Usage

1. Add the library to `INSTALLED_APPS`:

    ```
    INSTALLED_APPS = (
        ...
        'channels_discord',
    )
    ```

2. Create a Consumer

    Create a new consumer by inheriting from `DiscordConsumer`:

    ```python
    from channels_discord import DiscordConsumer

    class MyDiscordConsumer(DiscordConsumer):
        def ready(self):
            """
            Optional hook for actions on connection to Discord
            """
            print('You are now connected to discord!')

        def my_custom_message(self):
            """
            Use built-in functions to send basic discord actions
            """
            self.send_action('dm', user_id='SOME_DISCORD_USER_ID', text='your message')
            self.send_action(
                'send_to_channel',
                channel_id='SOME_DISCORD_CHANNEL_ID',
                text='your message'
            )
    ```

3. Add your consumer(s) to your router

    You can use the `discord` type in channels `ProtocolTypeRouter` to connect your new consumer to the interface server, and ensure your `discord` messages are delivered to the right place:

    ```python
    from channels.routing import ProtocolTypeRouter
    from myapp.consumers import MyDiscordConsumer

    application = ProtocolTypeRouter({
        'discord': MyDiscordConsumer,
    })
    ```

4. Start the interface server

    The interface server can be started by simply running this in the command line:

    ```bash
    channels-discord
    ```

    The server requires that the `token` and `application` properties be set:

    - `token`: Either a bot auth token or a user access token from user OAuth access. For information on how to acquire these tokens, please see Discord's [developer documentation](https://discordapp.com/developers/docs/topics/oauth2).

    - `application`: An import string pointing to the location of your app's ASGI application. Hence, if your app was named `myapp`, contained an ASGI filed called `asgi.py`, and your ASGI application is named `my_application`, you could start the server by running:

    ```
    channels-discord -t 'MY_LONG_BOT_TOKEN' -a 'myapp.asgi:my_application'
    ```

    You can also set these values using the env variables `CHANNELS_DISCORD_APPLICATION` and `DISCORD_BOT_TOKEN`.
