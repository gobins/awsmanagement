import argparse
import logging
import sys
import os

from cliff.app import App
from cliff.commandmanager import CommandManager
from awsmanagement import client


class AwsManagementApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(AwsManagementApp, self).__init__(
            description='AWS Management App',
            version='0.1',
            command_manager=CommandManager('awsmanagement.app'),
            )

    def configure_logging(self):
        log_lvl = logging.DEBUG if self.options.debug else logging.WARNING
        logging.basicConfig(
            format="%(levelname)s (%(module)s) %(message)s",
            level=log_lvl)
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        if self.options.verbose_level <= 1:
            logging.getLogger('requests').setLevel(logging.WARNING)

    def initialize_app(self, argv):
        self.log.debug('Initializing App')
        self.client = client.Client(
                 aws_access_key_id=self.options.aws_access_key_id,
                 aws_secret_access_key=self.options.aws_secret_access_key,
                 aws_region=self.options.aws_region)

    def prepare_to_run_command(self, cmd):
        self.log.debug('Prepare to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('Clean up %s', cmd.__class__.__name__)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        argparse_kwargs = argparse_kwargs or {}

        parser = argparse.ArgumentParser(
            description=description,
            add_help=True,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            **argparse_kwargs
        )

        parser.add_argument(
            '--debug',
            default=False,
            help='Show tracebacks on errors.')

        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output. Can be repeated.',
        )

        parser.add_argument(
            '--aws_access_key_id',
            default=os.environ.get('AWS_ACCESS_KEY_ID'),
            dest='aws_access_key_id',
            help='AWS Access key ID')
        parser.add_argument(
            '--aws_secret_access_key',
            default=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            dest='aws_secret_access_key',
            help='AWS Secret Access Key')
        parser.add_argument(
            '--aws_region',
            default=os.getenv('REGION_NAME', 'ap-southeast-2'),
            dest='aws_region',
            help='AWS Region Name')

        return parser


def main(argv=sys.argv[1:]):
    awsapp = AwsManagementApp()
    return awsapp.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
