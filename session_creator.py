from basic_functions import *

project_name = "test_project1.rpp"
#set directory with the files
directory = './audio/'
distance = 2
filename = directory + project_name

######################
"""Program begins"""
######################

#load list from text file
files_to_load = import_list_of_files('list_of_files.txt')

# get the filenames from directory
all_files, wav_files = get_all_and_wave_filenames_from_directory(directory)

#compare list and real files
good_files, extra_files, files_not_present = \
compare_list_and_wave_files_in_directory(files_to_load, wav_files)

#self_explanatory
print_missing_and_extra_files(extra_files, files_not_present, directory)

#create wavefile objects from the good files
wavefiles = get_wavefile_objects(directory, good_files)

#basing on data from wavefiles generate dictionary,
#with parameters as keys, to allow auting
audit = generate_audit(wavefiles)

#print bad values
not_matching_parameters, long_files_and_lenghts = \
check_if_the_files_are_the_same(audit)


#generate final string
project = generate_reaper_project(wavefiles, distance)

#write it to file
with open(filename, 'w') as f:
    f.write(project)
