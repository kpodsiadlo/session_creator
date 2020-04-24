from basic_functions import *


project_name = "test_project1.rpp"
#set directory with the files
directory = './audio/'
distance = 2
filename = directory + project_name

######################
"""Program begins"""
######################

#get the filenames
files, waves = get_wave_filenames_from_directory(directory)
wavefiles = get_list_of_wavefiles(directory, waves)
audit(wavefiles)

#generate string containing items
items = create_all_items(wavefiles, distance)
track = create_track_with_items(items)
project = create_project(track, filename)


with open(filename, 'w') as f:
    f.write(project)
