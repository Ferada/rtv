import os
import sys
import locale
import logging

import requests
import praw
import praw.errors
from six.moves import configparser

from .docs import TITLE
from .config import config
from .exceptions import SubmissionError, SubredditError, ProgramError
from .curses_helpers import curses_session
from .submission import SubmissionPage
from .subreddit import SubredditPage

__all__ = []

def main():
    "Main entry point"

    # Unicode support
    locale.setlocale(locale.LC_ALL, '')

    # Squelch SSL warnings for Ubuntu
    logging.captureWarnings(True)

    # Set the title of the terminal window
    if os.name == 'nt':
        os.system('title {0}'.format(TITLE))
    else:
        sys.stdout.write("\x1b]2;{0}\x07".format(TITLE))

    config.initialize()

    if config['log']:
        logging.basicConfig(level=logging.DEBUG, filename=config['log'])

    try:
        print('Connecting...')
        reddit = praw.Reddit(user_agent=AGENT)
        reddit.config.decode_html_entities = False
        if config['username']:
            # PRAW will prompt for password if it is None
            reddit.login(config['username'], config['password'])
        with curses_session() as stdscr:
            if config['submission']:
                page = SubmissionPage(stdscr, reddit, url=config['submission'])
                page.loop()
            page = SubredditPage(stdscr, reddit, config['subreddit'])
            page.loop()
    except praw.errors.InvalidUserPass:
        print('Invalid password for username: {}'.format(args.username))
    except requests.ConnectionError:
        print('Connection timeout')
    except requests.HTTPError:
        print('HTTP Error: 404 Not Found')
    except SubmissionError as e:
        print('Could not reach submission URL: {}'.format(e.url))
    except SubredditError as e:
        print('Could not reach subreddit: {}'.format(e.name))
    except ProgramError as e:
        print('Error: could not open file with program "{}", '
              'try setting RTV_EDITOR'.format(e.name))
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure sockets are closed to prevent a ResourceWarning
        reddit.handler.http.close()

sys.exit(main())
