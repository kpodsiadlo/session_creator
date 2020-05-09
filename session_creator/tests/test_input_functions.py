import context
import unittest
from input_functions import *


class test_get_column_and_cells(unittest.TestCase):

    def test_valid_value(self):
        self.assertEqual(get_column_and_cells('A23:150'), ('a', ('23', '150')))

    def test_wrong_row_range(self):
        with self.assertRaises(ValueError):
            get_column_and_cells('A1000:5')

    def test_random_data(self):
        with self.assertRaises(ValueError):
            get_column_and_cells('stefan')


class test_parse_cli_arguments(unittest.TestCase):

    def test_parses_valid_input_excel(self):

        arguments = [
         "tests/resources/input_files/file_list.xlsx",
         "tests/resources/cliout.rpp", "tests/resources/test_audio", "-d",
         "3", "-r", "C2:8"]

        results = (
         "tests/resources/input_files/file_list.xlsx",
         "tests/resources/cliout.rpp", "tests/resources/test_audio", 3.0,
         "c", ('2', '8'))

        self.assertEqual(parse_cli_arguments(arguments), results)

    def test_parses_valid_input_txt(self):

        arguments = [
         "tests/resources/input_files/file_list.txt",
         "tests/resources/cliout.rpp", "tests/resources/test_audio", "-d",
         "3.987"]

        results = (
            "tests/resources/input_files/file_list.txt",
            "tests/resources/cliout.rpp", "tests/resources/test_audio", 3.987,
            None, (None, None))

        self.assertEqual(parse_cli_arguments(arguments), results)


#    def test_empty_input(self):
#        with self.assertRaises(SystemExit) as se:
#            parse_cli_arguments([])
#        self.assertEqual(se.exception.code, 2)
#
#    def less_than_three_parameters(self):
#        with self.assertRaises(SystemExit) as se:
#            parse_cli_arguments(['a', 'b'])
#        self.assertEqual(se.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
