import control.commands as commands


def handler(user_input):
    if commands.current_mode_local:
        print commands.current_local_path
    else:
        print commands.current_remote_path
