"""
Global configuration settings
"""

import os
import re
import copy
import argparse
import configparser
from collections import OrderedDict

from .docs import *

HOME = os.path.expanduser('~')
DEPRECATED_CONFIG = os.path.join(HOME, '.rtv')
XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))
XDG_CONFIG = os.path.join(XDG_CONFIG_HOME, 'rtv', 'rtv.cfg')

class Config(object):
    """
    Configuration object for storing and retrieving program settings.
    """

    # All valid config options should have a default defined here
    DEFAULTS = {
        'ascii': False,
        'config': None,
        'custom_commands': {},
        'log': None,
        'password': None,
        'username': None,
        'subreddit': 'front',
        'submission': None,
        }

    def __init__(self, defaults=None):

        self.data = defaults or copy.copy(self.DEFAULTS)
        self.filename = None

    def __getitem__(self, item):

        return self.data[item]

    def __setitem__(self, key, value):

        self.data[key] = value

    def load_args(self, args):
        "Load command line arguments from an argparse Namespace object."

        # Extract a dictionary and let empty values fall out
        settings = {k:v for k, v in vars(args).items() if v is not None}
        self.data.update(settings)

    def load_file(self, filename):
        "Load configuration settings from a file."

        parser = configparser.RawConfigParser()
        parser.read(filename)
        self.filename = filename

        if 'rtv' in parser.sections():
            settings = dict(parser.items('rtv'))
            # The config parser does not automatically handle boolean values
            if 'ascii' in settings:
                parser['rtv'].getboolean('ascii')
            self.data.update(settings)

        custom_commands = OrderedDict()
        for section in parser.sections():
            if section.startswith('open-'):
                pattern = parser.get(section, 'pattern').strip()
                prog = re.compile(pattern)
                command = parser.get(section, 'command')
                background = parser.getboolean(section, 'background')
                url_map[prog] = {
                    'pattern': pattern,
                    'command': command,
                    'background': background}
        self.data['custom_commands'] = url_map

    def initialize(self):

        parser = self.build_command_line_parser()
        args = parser.parse_args()

        # Search for the best config filepath to load
        for filename in [args.config, XDG_CONFIG, DEPRECATED_CONFIG]:
            if filename and os.path.exists(filename):
                self.load_file(filename)
                break

        # Then load from command line arguments; these always take priority
        # over config file settings
        self.load_args(args)

    @staticmethod
    def build_command_line_parser():

        parser = argparse.ArgumentParser(
            prog='rtv', description=SUMMARY, epilog=CONTROLS+HELP,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('-s', dest='subreddit', help='subreddit name')
        parser.add_argument('-l', dest='link', help='full link to a submission')
        parser.add_argument('--ascii', action='store_true',
                            help='enable ascii-only mode')
        parser.add_argument('--log', metavar='FILE', action='store',
                            help='Log HTTP requests to file')
        parser.add_argument('--config', metavar='FILE',
                            help='Path to a custom RTV config file')

        group = parser.add_argument_group('authentication (optional)', AUTH)
        group.add_argument('-u', dest='username', help='reddit username')
        group.add_argument('-p', dest='password', help='reddit password')

        return parser

config = Config()