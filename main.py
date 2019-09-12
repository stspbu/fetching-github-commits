from commands.base import process_actions
from commands.exceptions import *


def main():
    try:
        process_actions()
    except CommandNotFoundException:
        print('Error! No such command!')
    except IncorrectParamsException:
        print('Error! Incorrect params!')
    except MissingParamsException:
        print('Error! Missing params!')
    except CommandsException:
        print('Error!')
    # let other exceptions to be shown


if __name__ == '__main__':
    main()
