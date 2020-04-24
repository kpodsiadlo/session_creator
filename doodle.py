from basic_functions import *
from wavefile import Wavefile

"""items = []
for i in range(6):
    item = create_item()
    items.append(item)


track = create_track_with_items(items)

create_project(track, 'project.rpp')


directory = './audio/'
files, waves = get_wave_filenames_from_directory(directory)
wave_objects = read_waves(directory, waves)"""

new_track = create_track()
with open('new_track.txt', 'w') as f:
    f.write(new_track)
