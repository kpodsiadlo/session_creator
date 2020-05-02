import os
import sys

from input import *
from process import *
from reaper_output import *

sys.tracebacklimit = 10


# length of a dummy region if file does not exist

dummy_length = 3  # seconds

######################
"""Program begins"""
######################

if __name__ == '__main__':

    """Read files"""
    (list_file, target_dir, target_name, directory, distance_multiplier, 
     column, row_range) = parse_arguments()

    if list_file[-3:] == 'txt':
        files_to_load = import_list_of_files(list_file)
    elif list_file[-3:] == 'xls' or 'xlsx':
        files_to_load = get_filenames_from_excel_column(
            list_file, column, row_range[0], row_range[1])

    # get the filenames from directory
    all_files, wav_files = get_all_and_wave_filenames_from_directory(directory)

    """Process and analyze"""

    # compare text list and real files and print results
    good_files, extra_files, files_not_present = \
        compare_list_and_wave_files_in_directory(
            files_to_load, wav_files, directory)

    # create wavefile objects from the good files and create dummies
    wavefiles = create_wavefile_objects(files_to_load, good_files, directory)

    # inpect wavefiles for inconsistencies and print results
    inspect_files(wavefiles)

    """Write"""
    # generate final string
    project = generate_reaper_project(wavefiles, distance_multiplier)

    # write it to file
    with open(directory + "/" + target_name, 'w') as f:
        f.write(project)
