import os
import argparse

from excel_parsing import get_filenames_from_excel_column


def parse_arguments():
    """Parse arguments given to the script.
    Check if the arguments are valid filenames and directories.
    Return list of files to load, name of target project and directory with
    the audio files"""

    help_description = """Automatic creator of DAW session files from file list.
    Currently supports imports from Excel spreadsheets and text files
    and outputs to a Reaper session format."""

    parser = argparse.ArgumentParser(description = help_description)
    parser.add_argument('input_file', type=str, help='Input file: txt or xls/xls.')
    parser.add_argument('output_file', type=str, help='Input file: RPP (Reaper).')
    parser.add_argument('wave_folder', type=str, help='Directory with audio files.')
    args = parser.parse_args()
    args = vars(args)
    print(args['input_file'])


    if os.path.isfile(args['input_file']):
        list_file = args['input_file']
    else:
        raise IOError(f"File {args['input_file']} not found")

    #get the name of the output file
    try:
        directory, target_name = os.path.split(args['output_file'])
    except:
        raise IOError(f"Path {args['output_file']} is invalid")

    #Check if folder with files exists
    if os.path.isdir(args['wave_folder']):
        directory = args['wave_folder']
    else:
        raise IOError(f"File {args['wave_folder']} is not a valid path")

    return list_file, target_name, directory


def import_list_of_files(filename):
    """Generates a list of files from a text file. Expects each name to be in
    different line"""
    files = []
    with open(filename) as f:
        for line in f:
            files.append(line.rstrip())

    return files


def get_all_and_wave_filenames_from_directory(directory='./audio'):
    filenames = os.listdir(directory)
    wav_files = [file for file in filenames if file[-4:] == '.wav']
    return filenames, wav_files
