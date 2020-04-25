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


def create_project(track):
    with open('skeleton.txt') as f:
        skeleton = f.read()
    project = skeleton[:-2] + track + skeleton [-2:]
    return project


def generate_reaper_project(wavefiles, distance):
    items = create_all_items(wavefiles, distance)
    track = create_track_with_items(items)
    project = create_project(track)
    return project


def get_all_and_wave_filenames_from_directory(directory='./audio'):
    filenames = os.listdir(directory)
    wav_files = [file for file in filenames if file[-4:] == '.wav']
    return filenames, wav_files


def write_filenames(files):
    with open('list_of_files.txt', 'w') as f:
        for name_of_wav in files:
            f.write(name_of_wav + '\n')


def get_wavefile_objects(directory, wav_files):
    """Reads the list of wave files in the directory and returns a list of
    Wavefiles (class with properties of the wave file)"""
    wave_objects_list = []
    for filename in wav_files:
        wave_objects_list.append(Wavefile(directory, filename))
    return wave_objects_list


def generate_audit(wave_objects_list):
    """Generate a dictionary with wav file parameters as keys"""
    data = {}
    for wavefile in wave_objects_list:
        (filename, channels, sampwidth,
                    framerate, length_in_seconds) = wavefile.get_info()

        data[filename] = {'channels': channels,
                        'sampwidth': sampwidth,
                        'framerate':framerate,
                        'length_in_seconds':length_in_seconds}

    """create a defaultdict, taking as default result of a function
    returinng a defaultdict that takes as default result of a function
    returning an empty list
    """
    audit = defaultdict(lambda: defaultdict(list))
    for file, pv_dict in data.items():
        for parameter, value in pv_dict.items():
            audit[parameter][value].append(file)

    pprint(dict(audit))
    return audit


def check_if_the_files_are_the_same(audit):
    """Check if all the files have the same frequency, bitrate and number of
     channels."""

    # for lenth of the files
    not_matching_parameters = []
    for parameter in audit.keys():

        if parameter == 'length_in_seconds':
            long_files_and_lenghts = look_for_long_files(audit, parameter)

        else:
            #sprawdz czy wszystkie pliki sa takie same.
            if len(set(audit[parameter].keys())) == 1:
                print(f'All files have the same {parameter}')
            else:
                print(f'Not all the files have the same {parameter}')
                not_matching_parameters.append(parameter)

    return not_matching_parameters, long_files_and_lenghts


def look_for_long_files(audit, parameter):
    long_files_and_lenghts = []
    for length_in_seconds in audit[parameter]:
        if length_in_seconds > 4:
            long_files_and_lenghts.append((audit[parameter][length_in_seconds],
            length_in_seconds))

            #long_files_and_lenghts.append()
    return long_files_and_lenghts


def import_list_of_files(filename):
    files = []
    with open(filename) as f:
        for line in f:
            files.append(line.rstrip())

    return files


def compare_list_and_wave_files_in_directory(files_to_load, wav_files):
    """Return list of required files not present in directory and list of
    files in the directory not present in the list of required"""
    missing_files = set(files_to_load) - set(wav_files)
    extra_files = set(wav_files) - set(files_to_load)
    return list(missing_files), list(extra_files)


def print_missing_and_extra_files(missing_files, extra_files, directory):
    if len(missing_files) != 0:
        print(f"The following files are missing in ''{directory}': {missing_files}")
    if len(extra_files) != 0:
        print(f"The following files found in {directory}' folder "
        f"are not on the list: {extra_files}")
