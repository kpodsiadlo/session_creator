import os
import sys
import argparse
import re
from textwrap import dedent

from excel_parsing import get_filenames_from_excel_column
import settings as st


def parse_cli_arguments(arguments):  # CLI ONLY

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
        '--range', '-r', nargs='?', type=str, default=None,
        help='Spreadsheet column (single) and rows, e.g. "A2:20"')

    args = parser.parse_args(arguments)

    list_file_path = args.input_file_path
    output_file_path = args.output_file_path
    directory = args.audio_directory
    distance_multiplier = args.dist

    if args.range:
        column, row_range = get_column_and_cells(args.range)
    else:
        column, row_range = None, (None, None)

# print(list_file_path, output_file_path, directory, distance_multiplier,
#        column, row_range)
    return (list_file_path, output_file_path, directory, distance_multiplier,
            column, row_range)


def get_column_and_cells(spreadsheet_range):  # CLI ONLY
    """Check if excel range is in correct format and get the column and row
    range"""
    spreadsheet_range = spreadsheet_range.lower()

    if re.match('[a-z][0-9]+:[0-9]+', spreadsheet_range):
        column = spreadsheet_range[0]
        rows = re.findall('[0-9]+', spreadsheet_range)
        row_range = (rows[0], rows[1])

        # keeping it str for compatibility with the GUI
        if int(rows[0]) > int(rows[1]):
            raise ValueError("End row number must be "
                             + "greater that start row number.")
        else:
            return column, row_range

    else:
        raise ValueError("Spreadsheet range must be in [column]"
                         + "[start_row]:[end_row] (eg. 'A1:10') format.""")


def validate_input(list_file, output_file_path, directory,
                   distance_multiplier, column, row_range):
    errors = []

    if os.path.isfile(list_file):  # if file exist:

        # if invalid type:
        extension = os.path.splitext(list_file)[1]
        if not any(extension in st.input_formats[ext_type]
                   for ext_type in st.input_formats):
            errors.append("List_file_unknown_format.")

        # if is a spreadsheet, validate cell range input
        if extension in st.input_formats['spreadsheet']:
            row_start, row_stop, errors = validate_excel_range(
                                                column, row_range, errors)

    else:  # if file does not exist:
        errors.append("List_file_missing")

    if not os.path.isdir(directory):  # if audio folder does not exist:
        errors.append("Audio_directory_invalid")

    if not os.path.isdir(os.path.split(output_file_path)[0]):
        errors.append("Target_filepath_invalid")

    try:  # check if distance is a number
        distance_multiplier = float(distance_multiplier)
    except ValueError:
        errors.append("Distance_value_invalid")

    if errors:
        return errors, None, None
    else:
        return errors, (row_start, row_stop), distance_multiplier


def validate_excel_range(column, row_range, errors):

    try:

        if not column.isalpha():
            errors.append('Column_ID_invalid')  # check is column is valid
    except AttributeError:
        errors.append("Column_ID_missing")

    try:  # check if start...
        row_start = int(row_range[0])
    except TypeError:
        errors.append("Start_row_missing")
        row_start = None
    except ValueError:
        errors.append("Start_row_invalid")
        row_start = None

    try:  # ...and stop rows are valid
        row_stop = int(row_range[1])
    except TypeError:
        errors.append("Stop_row_missing")
        row_stop = None
    except ValueError:
        errors.append("Stop_row_invalid")
        row_stop = None

    if row_start and row_stop:
        if row_stop < row_start:
            errors.append("Stop_row_larger_than_start_row")

    return row_start, row_stop, errors


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
