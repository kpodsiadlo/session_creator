import os
import argparse
import re

from excel_parsing import get_filenames_from_excel_column


def parse_arguments():
    """Parse arguments given to the script.
    Check if the arguments are valid filenames and directories.
    Return list of files to load, name of target project and directory with
    the audio files"""

    help_description = """Automatic creator of DAW session files from the
    file list. Currently supports imports from Excel spreadsheets and
    text files and outputs to a Reaper session format."""

    parser = argparse.ArgumentParser(description=help_description)
    parser.add_argument(
        'input_file_path', type=str,
        help='Path to a file with the list of required files:txt or xls/xls.')
    parser.add_argument(
        'output_file_path', type=str,
        help='Path to an output file: suported filetype: .RPP (Reaper).')
    parser.add_argument(
        'audio_directory', type=str,
        help='Path to a directory with the audio files.')
    # Nargs gets additional arguments. "?" means get and return one argument
    parser.add_argument(
        '--dist', '-d', nargs='?', type=float,
        help=("Distance between regions as multiple\
        of the previous file's length."),
        default=2)
    parser.add_argument(
        '--range', '-r', nargs='?', type=str,
        help='Spreadsheet range, e.g. "A2:A20"')

    args = parser.parse_args()
    print(args)

    # check if input file exist
    if os.path.isfile(args.input_file_path):
        list_file = args.input_file_path
    else:
        raise IOError(f"File {args.input_file_path} not found")

    # get the name of the output file
    try:
        directory, target_name = os.path.split(args.output_file_path)
    except:
        raise IOError(f"Path {args.output_file_path} is invalid")

    # Check if folder with files exists
    if os.path.isdir(args.audio_directory):
        directory = args.audio_directory
    else:
        raise IOError(f"File {args.audio_directory} is not a valid path")

    # check is ds multiplier is a number
    try:
        distance_multiplier = float(args.dist)
    except:
        raise ValueError(f"Value {args.dist} is not a number")

    column, row_range = get_column_and_cells(args.range)

    return (list_file, target_name, directory, distance_multiplier, column,
            row_range)


def get_column_and_cells(spreadsheet_range):
    """Check if excel range is in correct format and get the column and row
    range"""
    spreadsheet_range = spreadsheet_range.lower()
    if re.match('[a-z][0-9]:[a-z][0-9]', spreadsheet_range):
        if spreadsheet_range[0] != spreadsheet_range[-2]:
            raise ValueError("You can load data from one column only!")
        elif int(spreadsheet_range[1]) > int(spreadsheet_range[-1]):
            raise ValueError("End row number must be \
                            greater that start row number")
        else:
            column = spreadsheet_range[0]
            row_range = (int(spreadsheet_range[1]), int(spreadsheet_range[-1]))
            return column, row_range
    else:
        raise ValueError("Spreadsheet range must be in 'A1:A10' format")


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
