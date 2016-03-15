import control.commands as commands


def handler(user_input):
    commands.current_mode_local = not commands.current_mode_local
