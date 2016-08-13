import sys

import control.commands as commands
import control.tools as tools
from control.commands import cd, cwd, dl, help, ls, mkdir, sw, up, exit


LINE_START_LOCAL = "$l "
LINE_START_REMOTE = "$r "


command_handlers = {
    'help': help.handler,
    'cd': cd.handler,
    'ls': ls.handler,
    'mkdir': mkdir.handler,
    'cwd': cwd.handler,
    'up': up.handler,
    'dl': dl.handler,
    'sw': sw.handler,
    'exit': exit.handler
}


def print_startup_message():
    """
    Welcome message of the script making it possible
    Returns: What the user wishes to do.
        "sync" synchronize state of folder with Google Drive.
    """

    print "Welcome to CloudDrive!\n\n"


def print_line_start():
    """
    Prints the beginning of each command-enabled line, to indicate whether current mode is local or remote.
    Returns: None
    """
    if commands.current_mode_local:
        start = tools.getRed(LINE_START_LOCAL)
    else:
        start = tools.getCyan(LINE_START_REMOTE)

    sys.stdout.write(start)


def execute_command():
    print_line_start()

    input_string = raw_input()
    input_string.strip()

    split_input = input_string.split(" ")
    command = split_input[0]

    if command in command_handlers.keys():
        command_handlers[command](split_input)  # execute command if command found.
        return True
    else:
        # Print help message if command entered incorrectly.
        print "Command {} not found. Type help to get an overview of all possible commands.".format(command)
        return False


# --- Entry point. ---
def run_cli():
    print_startup_message()
    commands.fetch_metadata()

    while True:
        success = execute_command()

if __name__ == "__main__":
    run_cli()
