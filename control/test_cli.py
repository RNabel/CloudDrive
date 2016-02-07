import cli
from unittest import TestCase


class CliTester(TestCase):
    def cd_handler_test(self):
        curr_path = cli.current_local_path

        func_input = ['', 'Documents']  # Documents has to exist.
        cli.cd_handler(func_input)
        self.assertTrue(curr_path + "/Documents" == cli.current_local_path)

        func_input = ['', '..']
        cli.cd_handler(func_input)
        self.assertTrue(curr_path == cli.current_local_path)
