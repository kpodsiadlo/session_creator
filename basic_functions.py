from uuid import uuid4
import os
from wavefile import Wavefile
from pprint import pprint
from collections import defaultdict

def create_empty_track():
    """Creates a track string"""
    id = str(uuid4()).upper()

    with open('track.txt', 'r') as f:
        track = f.readlines()
    #multiple {{{ to escape "{}" formatting
    track[0]  = f"  <TRACK {{{id}}}\n"
    track[20] = f"    TRACKID {{{id}}}\n"

    new_track = "".join(track)
    return new_track


def create_all_items(wavefiles, distance):
    "Create a string represeting all the files in project "
    position = 1
    items = ""
    for wavefile in wavefiles:
        items += create_item(wavefile, position)
        position += (wavefile.length_in_seconds +
                    distance *wavefile.length_in_seconds)

    return items


def create_item(wavefile, position):
    """Create a string representing a file"""
    iguid = str(uuid4()).upper()
    guid = str(uuid4()).upper()

    with open('item.txt', 'r') as f:
        item = f.readlines()
        item[1] =  f"          POSITION {position}"
        item[3]  = f"          LENGTH {wavefile.length_in_seconds}\n"
        item[10] = f"          IGUID {{{iguid}}}\n"
        item[12] = f"          NAME {wavefile.name}\n"
        item[17] = f"          GUID {{{guid}}}]\n"
        item[20] = f'           FILE "{wavefile.name}"\n'
    new_item = "".join(item)
    return new_item


def create_track_with_items(items): #items = string:
    track = create_empty_track()
    track = track[:-2] + items + track[-2:]
    return track


def create_project(track, filename):
    with open('skeleton.txt') as f:
        skeleton = f.read()
    project = skeleton[:-2] + track + skeleton [-2:]
    return project


def get_wave_filenames_from_directory(directory='./audio'):
    filenames = os.listdir(directory)
    wav_files = [file for file in filenames if file[-4:] == '.wav']
    return filenames, wav_files


def get_list_of_wavefiles(directory, wav_files):
    """Reads the list of wave files in the directory and returns a list of
    Wavefiles (class with properties of the wave file)"""
    wave_objects_list = []
    for filename in wav_files:
        wave_objects_list.append(Wavefile(directory, filename))
    return wave_objects_list


def audit(wave_objects_list):
    data = {}
    for wavefile in wave_objects_list:
        (filename, channels, sampwidth,
                    framerate, length_in_seconds) = wavefile.get_info()

        data[filename] = {'channels': channels,
                        'sampwidth': sampwidth,
                        'framerate':framerate,
                        'length_in_seconds':length_in_seconds}

        # audit przypisz default dict. Lambda, bo musi być funkcja
        # jako parametr do defaultdict. List, bo cośtam
    audit = defaultdict(lambda: defaultdict(list))
    for file, pv_dict in data.items():
        for parameter, value in pv_dict.items():
            audit[parameter][value].append(file)

    pprint(dict(audit))







#generate list of all channel, samplerate and framerate types in the dictionary:
"""    channel_types = set()
    sampwidth_types = set()
    framerate_types = set()

    for parameters in data.values():
        channel_types.add(parameters['channels'])
        sampwidth_types.add(parameters['sampwidth'])
        framerate_types.add(parameters['framerate'])


    audit = {}
    for type in channel_types:
        list_of_files = []
        print(data.items()  )
        for key, value in data.items():
            if value['channels'] == type:
                list_of_files.append(key)
            audit['channels'] = {type: list_of_files}


    pprint(data)
    pprint(audit)
    pprint(channel_types)"""
