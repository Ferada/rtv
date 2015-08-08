"""
Global configuration settings
"""

import os
import argparse
from .docs import *

# 1.) Load the command line arguments
# 2.) Load the config file from the command line arguments, then default path
# 3.) Overwrite config file values with command line arguments


# 1.) Load the config file(s) first, falling back to a default config file somewhere
# 2.) Load the command line arguments


HOME = os.path.expanduser('~')
XDG_HOME = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))
CONFIG = os.path.join(XDG_HOME, 'rtv', 'rtv.cfg')

# Fall back to the old config path for compatibility
CONFIG_DEPRECATED = os.path.join(HOME, '.rtv')


def build_parser():
    parser = argparse.ArgumentParser(
        prog='rtv', description=SUMMARY, epilog=CONTROLS+HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-s', dest='subreddit', help='subreddit name')
    parser.add_argument('-l', dest='link', help='full link to a submission')
    parser.add_argument('--ascii', action='store_true',
                        help='enable ascii-only mode')
    parser.add_argument('--log', metavar='FILE', action='store',
                        help='Log HTTP requests')
    parser.add_argument('--config', metavar='FILE', action='store',
                        help='Location of config file')

    group = parser.add_argument_group('authentication (optional)', AUTH)
    group.add_argument('-u', dest='username', help='reddit username')
    group.add_argument('-p', dest='password', help='reddit password')
    return parser


class Config(dict):



    def load(self, *args):
        pass


config = Config()





unicode = True


def load_config():
    """
    Search for a configuration file at the location ~/.rtv and attempt to load
    saved settings for things like the username and password.
    """

    config = configparser.ConfigParser()


    config_paths = [
        os.path.join(XDG_CONFIG_HOME, 'rtv', 'rtv.cfg'),
        os.path.join(HOME, '.rtv')
    ]

    # read only the first existing config file
    for config_path in config_paths:
        if os.path.exists(config_path):
            config.read(config_path)
            break

    defaults = {}
    if config.has_section('rtv'):
        defaults = dict(config.items('rtv'))

    if 'ascii' in defaults:
        defaults['ascii'] = config.getboolean('rtv', 'ascii')

    return defaults

# Fill in empty arguments with config file values. Paramaters explicitly
# typed on the command line will take priority over config file params.
for key, val in local_config.items():
    if getattr(args, key, None) is None:
        setattr(args, key, val)

config.unicode = (not args.ascii)

args = command_line()
local_config = load_config()


def load_config():
    """
    Search for a configuration file at the location ~/.rtv and attempt to load
    saved settings for things like the username and password.
    """

    config = configparser.ConfigParser()

    HOME = os.path.expanduser('~')
    XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))
    config_paths = [
        os.path.join(XDG_CONFIG_HOME, 'rtv', 'rtv.cfg'),
        os.path.join(HOME, '.rtv')
    ]

    # read only the first existing config file
    for config_path in config_paths:
        if os.path.exists(config_path):
            config.read(config_path)
            break

    defaults = {}
    if config.has_section('rtv'):
        defaults = dict(config.items('rtv'))

    if 'ascii' in defaults:
        defaults['ascii'] = config.getboolean('rtv', 'ascii')

    return defaults
