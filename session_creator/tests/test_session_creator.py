import context
import unittest
import os
import settings as st
from user_input import UserInput
from session_creator import main

root = os.getcwd()

list_file_path = os.path.join(root, st.gui_default_input_path)
audio_directory = os.path.join(root, st.gui_default_audio_folder)
output_file_path = os.path.join(root, st.gui_default_output_path)
distance_multiplier = 3
column = "C"
row_range = ("3", "7")

class TestMain(unittest.TestCase):

    def test_main_excel_correct_values(self):
        self.user_input = UserInput(list_file_path, output_file_path, 
        audio_directory, distance_multiplier, column, row_range)
        result = main(self.user_input)
        self.assertIn("REAPER", result)


    def test_main_no_input(self):
        self.user_input = UserInput()
        with self.assertRaises(UnboundLocalError):
             main(self.user_input)
