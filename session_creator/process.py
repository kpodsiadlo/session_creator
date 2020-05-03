from collections import defaultdict

from wavefile import Wavefile


def create_wavefile_objects(files_to_load, good_files, directory):
    """Reads the list of wave files in the directory and returns a list of
    Wavefiles (class with properties of the wave file)"""
    wave_objects_list = []
    for filename in files_to_load:
        if filename in good_files:
            wave_objects_list.append(Wavefile(filename, directory))
        else:
            wave_objects_list.append(create_dummy(filename))

    return wave_objects_list


def create_dummy(filename):
    dummy = Wavefile(filename)
    return dummy


def inspect_files(wave_objects_list):
    """Generate a dictionary with wav file parameters as keys."""
    data = {}
    for wavefile in wave_objects_list:
        (filename, channels, sampwidth,
         framerate, length_in_seconds) = wavefile.get_info()

        data[filename] = {'channels': channels,
                          'sampwidth': sampwidth,
                          'framerate': framerate,
                          'length_in_seconds': length_in_seconds}

    """Create a defaultdict, taking as default result of a function
    returning a defaultdict that takes as default result of a function
    returning an empty list
    """
    audit = defaultdict(lambda: defaultdict(list))
    for file, pv_dict in data.items():
        for parameter, value in pv_dict.items():
            audit[parameter][value].append(file)

    check_if_the_files_are_the_same(audit)
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
            # check if all the files have the same length.
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

    if long_files_and_lenghts:
        print(f'Long files: {long_files_and_lenghts}')

    return long_files_and_lenghts


def compare_list_and_wave_files_in_directory(
                                    files_to_load, wav_files, directory):
    """Return list of required files not present in directory and list of
    files in the directory not present in the list of required"""
    good_files = [item for item in files_to_load if item in wav_files]
    missing_files = [item for item in files_to_load if item not in wav_files]
    extra_files = [item for item in wav_files if item not in files_to_load]
    print_missing_and_extra_files(missing_files, extra_files, directory)

    return good_files, missing_files, extra_files


def print_missing_and_extra_files(missing_files, extra_files, directory):
    if len(missing_files) != 0:
        print(f"The following files     "
              f"are missing in '{directory}': {missing_files}")
    if len(extra_files) != 0:
        print(f"The following files found in {directory}' folder "
              f"are not on the list: {extra_files}")
