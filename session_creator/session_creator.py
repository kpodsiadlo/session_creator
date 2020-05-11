import os
import sys

from input_functions import (parse_cli_arguments, import_list_of_files,
                             get_filenames_from_excel_column,
                             get_all_and_wave_filenames_from_directory)
from process import (create_wavefile_objects, inspect_files,
                     compare_list_and_wave_files_in_directory)
from reaper_output import generate_reaper_project
import settings as st
from user_input import UserInput


def main(user_input):

    files_to_load, wav_files, good_files = get_files(user_input)

    """Create and inspect wavefiles"""

    # create wavefile objects from the good files and create dummies
    wavefiles = create_wavefile_objects(files_to_load, good_files,
                                        user_input.audio_directory)

    # inpect wavefiles for inconsistencies and print results
    inspect_files(wavefiles)

    """Write"""
    # generate final string
    project = generate_reaper_project(
        wavefiles, user_input.distance_multiplier)

    # write it to file
    with open(user_input.output_file_path, 'w') as f:
        f.write(project)

    return project


def get_files(user_input):

    if user_input.list_file_type == 'text':
        files_to_load = import_list_of_files(user_input.list_file_path)
    elif user_input.list_file_type == 'spreadsheet':
        files_to_load = get_filenames_from_excel_column(user_input)

    # get the filenames from directory
    all_files, wav_files = get_all_and_wave_filenames_from_directory(
        user_input.audio_directory)

    # compare text list and real files and print results
    good_files, extra_files, files_not_present = \
        compare_list_and_wave_files_in_directory(
            files_to_load, wav_files, user_input.audio_directory)

    return files_to_load, wav_files, good_files


# For CLI use
if __name__ == '__main__':

    arguments = sys.argv[1:]

    """Read files"""
    (list_file_path, output_file_path, directory, distance_multiplier,
     column, row_range) = parse_cli_arguments(arguments)

    user_input = UserInput(list_file_path, output_file_path, directory,
                           distance_multiplier, column, row_range)

    if user_input.errors:
        print(f"User input: {user_input.errors}")
        print('"python3 session_creator.py -h" for help.')

    else:
        main(user_input)
