import control.tools as tools
import control.commands as commands


def handler(user_input):
    files, folders = commands.get_current_folder_contents()

    output_string = ""
    if files:
        output_string += tools.getYellow(u"Files:\n{}{}".format("'" + "' '".join(files) + "'", "\n" if folders else ""))
    if folders:
        output_string += tools.getLightPurple(u"Folders:\n{}".format("'" + "' '".join(folders) + "'"))

    print output_string
