from basic_functions import *

project_name = "test_project1.rpp"
#set directory with the files
directory = './audio/'
distance = 2
filename = directory + project_name

######################
"""Program begins"""
######################

files_to_load = import_list_of_files('list_of_files.txt')
print(files_to_load)

#get the filenames
all_files, wav_files = get_all_and_wave_filenames_from_directory(directory)
wavefiles = get_wavefile_objects(directory, wav_files)

extra_files, files_not_present = compare_list_and_wave_files_in_directory(files_to_load, wav_files)
print_missing_and_extra_files(extra_files, files_not_present, directory)
"""
write_filenames(wave_files)



#audit = generate_audit(wavefiles)
#not_matching_parameters, long_files_and_lenghts = check_if_the_files_are_the_same(audit)


#print(f'Parameters not matching: {not_matching_parameters}\n'
        #f'Long files: {long_files_and_lenghts}')


#generate final string
project = generate_reaper_project(wavefiles, distance)
with open(filename, 'w') as f:
    f.write(project)"""
