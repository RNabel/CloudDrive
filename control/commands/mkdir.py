import os
import control.commands as commands
import cloud_interface.file_sync as file_sync


def handler(user_input):
    folder_name = " ".join(user_input[1:])

    if commands.current_mode_local:
        # Create local folder.
        os.mkdir(commands.current_local_path + "/" + folder_name)
    else:
        file_sync.create_folder(folder_name, commands.current_remote_dir_id)
        # Update metadata.
        commands.fetch_metadata()
