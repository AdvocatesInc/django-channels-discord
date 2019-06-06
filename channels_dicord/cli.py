import argparse
import logging

from .client import ChannelsDiscordClient


class CLI(object):
    """
    Primary command-line interface for Discord -> channels bridge
    """
    description = "Django Channels <-> Discord Interface server"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=self.description,
        )
        self.parser.add_argument(
            '-a',
            '--application',
            dest='application',
            help='The django channels application as path.to.module:instance.path',
            default=os.environ.get('CHANNELS_DISCORD_APPLICATION', None),
        )
        self.parser.add_argument(
            '-t',
            '--token',
            dest='token',
            help='OAuth or Bot token used to connect to discord',
            default=os.environ.get('DISCORD_BOT_TOKEN', None),
        )
        self.parser.add_argument(
            '-v',
            '--verbosity',
            type=int,
            help='How verbose to make the output. Default is 1',
            default=1,
        )

    @classmethod
    def entrypoint(cls):
        """
        Many entrypoint for external starts
        """
        cls().run(sys.argv[1:])

    def run(self, args):
        """
        Mounts the Discord interface server based on the raw arguments passed in
        """
        args = self.parser.parse_args(args)

        # Set up logging
        logging.basicConfig(
            level={
                0: logging.WARN,
                1: logging.INFO,
                2: logging.DEBUG,
            }[args.verbosity],
            format="%(asctime)-15s %(levelname)-8s %(message)s",
        )

        # import the channel layer
        asgi_module, application_path = args.application.split(':', 1)
        application_module = importlib.import_module(asgi_module)
        for part in application_path.split('.'):
            application = getattr(application_module, part)

        client = ChannelsDiscordClient(application)
        client.run(token=args.token)
