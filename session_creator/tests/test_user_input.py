import context
import unittest
import os
import settings as st
from user_input import UserInput

root = os.getcwd() + "/"


class TestUserInput(unittest.TestCase):

    def setUp(self):
        self.user_input = UserInput()
        self.user_input.errors = []

    def test___init__(self):
        parameters = (
            root + st.gui_default_input_path,
            root + st.gui_default_output_path,
            root + st.gui_default_audio_folder, 3.0,
            "c", ('2', '8'))
        self.user_input = UserInput(*parameters)
        self.assertFalse(self.user_input.errors)

    def test_validate_list_file_not_a_file(self):

        result = self.user_input.validate_list_file("Test_string")
        self.assertEqual(result, ("Test_string", None))
        self.assertIn("Input file not found.", self.user_input.errors)

    def test_validate_list_file_good_file(self):

        test_file = root + st.gui_default_input_path
        fpath, ftype = self.user_input.validate_list_file(test_file)
        print(fpath, ftype)
        self.assertEqual(fpath, test_file)
        self.assertEqual(ftype, 'spreadsheet')
        self.assertFalse(self.user_input.errors)

    def test_get_list_file_type_wrong_type(self):

        self.user_input.get_list_file_type("ciapki.csv")
        self.assertEqual("Unknown input file type.",
                         self.user_input.errors[-1])

    def test_get_list_file_type_excel(self):

        test_file = root + st.gui_default_input_path
        result = self.user_input.get_list_file_type(test_file)
        self.assertEqual(result, "spreadsheet")

    def test_get_list_file_type_txt(self):

        test_file = root + "test/resources/input_files/file_list.txt"
        result = self.user_input.get_list_file_type(test_file)
        self.assertEqual(result, "text")

    def test_validate_output_file_not_a_path(self):
        self.user_input = UserInput()
        self.user_input.validate_output_file("None")
        self.assertEqual("Wrong output file path.", self.user_input.errors[-1])

    def test_validate_output_file_type(self):
        result = self.user_input.validate_output_file_type("test.rpp")
        self.assertFalse(self.user_input.errors)
        self.assertEqual(result, "Reaper")

    def test_validate_directory_wrong_directory(self):
        result = self.user_input.validate_directory("Test directory")
        self.assertIn("Invalid audio directory path.", self.user_input.errors)
        self.assertEqual(result, None)

    def test_validate_directory_good_directory(self):
        result = self.user_input.validate_directory("/usr/bin")
        self.assertEqual("/usr/bin", result)
        self.assertFalse(self.user_input.errors)

    def test_validate_distance_multiplier(self):
        pass

    def test_validate_excel_range(self):
        pass


if __name__ == '__main__':
    unittest.main()
