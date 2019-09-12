import re
import sys
import time

import settings
import commands.settings
from commands.exceptions import IncorrectParamsException, MissingParamsException, CommandNotFoundException
from github import GithubManager
from storager import PatchStorager, StatStorager


def on_fetch_command():
    if len(sys.argv) > 2:
        repo_url = sys.argv[2]
    else:
        raise MissingParamsException

    match = re.match(r'https?://github\.com/(\w+)/([\w\-.]+)/?', repo_url)
    if not match:
        raise IncorrectParamsException

    user_name, repo_name = match.groups()

    manager = GithubManager()
    patch_storager = PatchStorager()
    stat_storager = StatStorager()

    start_ts = int(time.time()*1e6)
    manager.load_commits(user_name, repo_name, limit=50, show_progress=True)

    authors = manager.get_authors()
    files = manager.get_files()

    patch_storager.store(files, start_ts)
    stat_storager.store(authors, files, start_ts)

    dir_path = f'{settings.get("folder", "files")}/{start_ts}'
    print(f'Files saved in dir: {dir_path}')
    print(f'Stats saved in file: {dir_path}/{settings.get("statfile", "stat")}.txt')


def on_help_command():
    print(
        'This script is fetching git commits into local files.\n'
        'It also shows a simple statistics about these commits.\n'
        '\n'
        'Usage: python3 main.py command1 command2...\n'
        'Available commands:\n'
        'help -- shows help\n'
        'fetch -- fetching commits\n'
        'settings -- shows settings help'
    )


def process_actions():
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = 'help'

    if command == 'help':
        on_help_command()
    elif command == 'fetch':
        on_fetch_command()
    elif command == 'settings':
        commands.settings.process_actions()
    else:
        raise CommandNotFoundException

