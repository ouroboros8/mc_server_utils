# Delete all files in a directory older than age.

import sys
import os
import argparse
from datetime import datetime, timedelta
import re

def error(string):
    print("Error: ", string, file=sys.stderr)

def str_to_timedelta(timedelta_string):
    timedelta_string_pattern = re.compile('\d*[smdw]')
    if not timedelta_string_pattern.fullmatch(timedelta_string):
        error(timedelta_string, " is not a correctly formatted time string.")
        sys.exit()
    else:
        unit = timedelta_string[-1]
        value = int(timedelta_string[:-1])
        if unit == 's':
            return timedelta(seconds=value)
        elif unit == 'm':
            return timedelta(minutes=value)
        elif unit == 'd':
            return timedelta(days=value)
        else:
            return timedelta(weeks=value)

def checkdir(dirstring):
    if not os.path.isdir(dirstring):
        error("Error: no such directory ", dirstring)
    else:
        return os.path.realpath(dirstring)

def main():
    time_help = '''
        an integer followed by a suffix, denoting units. Files created longer than t ago
        will be deleted. Suffixes 's', 'm', 'd', 'w' represent seconds, minutes, days,
        weeks, respectively.
        '''

    parser = argparse.ArgumentParser(description='Process command line options')
    parser.add_argument('timedelta', metavar='TIME', type=str_to_timedelta, help=time_help)
    parser.add_argument('directory', metavar='DIR', type=checkdir,
                        help='The directory to delete old files from')
    parser.add_argument('--dry', action='store_true',
                        help='run command, but don\'t delete files: instead, print a list'
                             ' of files to be deleted.')
    args = parser.parse_args()

    for f in os.listdir(args.directory):
        f = os.path.realpath(os.path.join(args.directory, f))
        if os.stat(f).st_mtime < datetime.timestamp(datetime.now() - args.timedelta):
            if os.path.isfile(f):
                if args.dry:
                    print(os.path.basename(f))
                else:
                    os.remove(f)

if __name__ == '__main__':
    main()
