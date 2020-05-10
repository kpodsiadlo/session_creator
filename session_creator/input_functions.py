import os
import sys
import argparse
import re
from textwrap import dedent

from excel_parsing import get_filenames_from_excel_column
import settings as st


def parse_cli_arguments(arguments):  # CLI ONLY

    """Parse arguments given to the script.
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


def import_list_of_files(filename):
    """Generates a list of files from a text file. Expects each name to be in
    different line"""
    files = []
    with open(filename) as f:
        for line in f:
            files.append(line.rstrip())

    return files


def get_all_and_wave_filenames_from_directory(directory):
    filenames = os.listdir(directory)
    wav_files = [file for file in filenames if file[-4:] == '.wav']

    return filenames, wav_files
