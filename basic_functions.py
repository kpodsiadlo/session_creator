from uuid import uuid4
import os
from wavefile import Wavefile

def create_track():
    id = str(uuid4()).upper()

    with open('track.txt', 'r') as f:
        track = f.readlines()
    #multiple {{{ to escape "{}" formatting
    track[0]  = f"  <TRACK {{{id}}}\n"
    track[20] = f"    TRACKID {{{id}}}\n"

    new_track = "".join(track)
    return new_track


def create_item():
    iguid = str(uuid4()).upper()
    guid = str(uuid4()).upper()

    with open('item.txt', 'r') as f:
        item = f.readlines()
        item[10] = "          IGUID {{{iguid}}}\n"
        item[17] = "          GUID {{{guid}}}]n"

    new_item = "".join(item)

    return new_item


def create_track_with_items(items): #items = list:
    track = create_track()
    for item in items:
        print(item)
        track = track[:-2] + item + track[-2:]
        print(len(track))
    return track

def create_project(track, filename):
    with open('skeleton.txt') as f:
        skeleton = f.read()

    project = skeleton[:-2] + track + skeleton [-2:]

    with open(filename, 'w') as f:
        f.write(project)


def get_wave_filenames_from_directory(directory='./audio'):
    filenames = os.listdir(directory)
    wav_files = [file for file in filenames if file[-4:] == '.wav']
    return filenames, wav_files

def read_waves(directory, wav_files):

    wave_object_list = []
    for filename in wav_files:
        path = directory + filename
        wave_object_list.append(Wavefile(path))

    return wave_object_list
