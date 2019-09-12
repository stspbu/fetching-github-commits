import json
import sys

import settings
from commands.exceptions import MissingParamsException, IncorrectParamsException, CommandNotFoundException


def on_get_command():
    print(json.dumps({
        'token': settings.get('token'),
        'folder': settings.get('folder', 'files'),
        'statfile': settings.get('statfile', 'stat'),
        'authorizedonly': settings.get('authorizedonly', '0')
    }, indent=4))


def on_set_command():
    if len(sys.argv) > 3:
        key_value = sys.argv[3]
    else:
        raise MissingParamsException

    try:
        key, value = key_value.split(':')
        if not value:
            raise ValueError
    except:
        raise IncorrectParamsException

    settings.set(key, value)


def on_list_command():
    print(
        'Available settings:\n'
        'folder -- folder, storing commit patches (default: files)\n'
        'token -- oauth token for github api, if requests limit exceeded\n'
        'statfile -- a file name, where last query statistics will be stored (default: stat)\n'
        'authorizedonly -- if set to 1, only authorized commit authors will be shown in stats (default: 0)'
    )


def on_help_command():
    print(
        'Program settings\n'
        'You can also change them using settings.json\n'
        '\n'
        'Usage: python3 main.py settings command1 command2...\n'
        'Available commands:\n'
        'help -- shows help\n'
        'list -- shows a list of settings with description\n'
        'set -- set a setting in key:value format (e.g. folder:commits)\n'
        'get -- shows all settings and their values (json format)'
    )


def process_actions():
    if len(sys.argv) > 2:
        command = sys.argv[2]
    else:
        command = 'help'

    if command == 'help':
        on_help_command()
    elif command == 'list':
        on_list_command()
    elif command == 'set':
        on_set_command()
    elif command == 'get':
        on_get_command()
    else:
        raise CommandNotFoundException
