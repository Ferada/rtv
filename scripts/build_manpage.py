"""
Internal tool used to automatically generate an up-to-date version of the rtv
man page. Currently this script should be manually ran after each version bump.
In the future, it would be nice to have this functionality built into setup.py.

Usage:
    $ python scripts/build_manpage.py
"""
import os
import sys
from datetime import datetime

_filepath = os.path.dirname(os.path.relpath(__file__))
ROOT = os.path.abspath(os.path.join(_filepath, '..'))
sys.path.insert(0, ROOT)

import rtv
from rtv import config

def main():
    parser = config.build_parser()
    help = parser.format_help()
    help_sections = help.split('\n\n')

    data = {}
    print('Fetching version')
    data['version'] = rtv.__version__
    print('Fetching release date')
    data['release_date'] = datetime.utcnow().strftime('%B %d, %Y')
    print('Fetching synopsis')
    synopsis = help_sections[0].replace('usage: ', '')
    synopsis = ' '.join(line.strip() for line in synopsis.split('\n'))
    data['synopsis'] = synopsis
    print('Fetching description')
    data['description'] = help_sections[1]
    # Build the options section for each argument from the help section
    # Example Before:
    #         -h, --help        show this help message and exit
    # Example After
    #         .TP
    #         \fB-h\fR, \fB--help\fR
    #         show this help message and exit
    options = ''
    arguments = help_sections[2].split('\n')
    for argument in arguments[1:]:
        argument = argument.strip()
        flag, description = (col.strip() for col in argument.split('  ', 1))
        flag = ', '.join(r'\fB'+f+r'\fR' for f in flag.split(', '))
        options += '\n'.join(('.TP', flag, description, '\n'))
    data['options'] = options
    print('Fetching license')
    data['license'] = rtv.__license__
    print('Fetching copyright')
    data['copyright'] = rtv.__copyright__
    # Escape dashes is all of the sections
    data = {k:v.replace('-', r'\-') for k,v in data.items()}
    print('Reading from %s/templates/rtv.1' % ROOT)
    with open(os.path.join(ROOT, 'templates/rtv.1')) as fp:
        template = fp.read()
    print('Populating template')
    out = template.format(**data)
    print('Writing to %s/rtv.1' % ROOT)
    with open(os.path.join(ROOT, 'rtv.1'), 'w') as fp:
        fp.write(out)

if __name__ == '__main__':
    main()