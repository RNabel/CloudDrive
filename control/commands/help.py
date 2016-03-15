import sys
import control.commands as commands
import control.tools as tools


def handler(user_input):
    output_string = ""

    for k, v in commands.available_options.iteritems():
        output_string += tools.getCyan(k) + "\t" + tools.getRed(v) + "\n"

    sys.stdout.write(output_string)
