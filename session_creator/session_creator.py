import os
import sys

from input_functions import *
from process import *
from reaper_output import *
import settings as st
from user_input import UserInput


def main(list_file_path, output_file_path, audio_directory,
         distance_multiplier, column, row_range):

    if list_file_path[-3:] == 'txt':
        files_to_load = import_list_of_files(list_file_path)
    elif list_file_path[-3:] == 'xls' or 'lsx':
        files_to_load = get_filenames_from_excel_column(
            list_file_path, column, row_range[0], row_range[1])

    # get the filenames from directory
    all_files, wav_files = get_all_and_wave_filenames_from_directory(
                                                            audio_directory)

    """Process and analyze"""

    # compare text list and real files and print results
    good_files, extra_files, files_not_present = \
        compare_list_and_wave_files_in_directory(
            files_to_load, wav_files, audio_directory)

    # create wavefile objects from the good files and create dummies
    wavefiles = create_wavefile_objects(files_to_load, good_files,
                                        audio_directory)

    # inpect wavefiles for inconsistencies and print results
    inspect_files(wavefiles)

    """Write"""
    # generate final string
    project = generate_reaper_project(wavefiles, distance_multiplier)

    # write it to file
    with open(output_file_path, 'w') as f:
        f.write(project)


# For CLI use
if __name__ == '__main__':

    arguments = sys.argv[1:]

    """Read files"""
    (list_file_path, output_file_path, directory, distance_multiplier,
     column, row_range) = parse_cli_arguments(arguments)

    errors, row_range, distance_multiplier = validate_input(
        list_file_path, output_file_path, directory, distance_multiplier,
        column, row_range)
        

    if errors:
        print(errors)
        print('"python3 session_creator.py -h" for help.')
    else:
        main(list_file_path, output_file_path, directory, distance_multiplier,
             column, row_range)
