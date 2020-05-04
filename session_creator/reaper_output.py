from uuid import uuid4


def create_empty_track():
    """Creates a track string"""
    id = str(uuid4()).upper()

    with open('resources/reaper/track.txt', 'r') as f:
        track = f.readlines()
    # multiple {{{ to escape "{}" formatting
    track[0] = f"  <TRACK {{{id}}}\n"
    track[20] = f"    TRACKID {{{id}}}\n"

    new_track = "".join(track)
    return new_track


def create_item(wavefile, position):
    """Create a string representing a file"""
    iguid = str(uuid4()).upper()
    guid = str(uuid4()).upper()

    with open('resources/reaper/item.txt', 'r') as f:
        item = f.readlines()
        item[1] = f"          POSITION {position}"
        item[3] = f"          LENGTH {wavefile.length_in_seconds}\n"
        item[10] = f"          IGUID {{{iguid}}}\n"
        item[12] = f"          NAME {wavefile.name}\n"
        item[17] = f"          GUID {{{guid}}}]\n"
        item[20] = f'           FILE "{wavefile.name}"\n'
    new_item = "".join(item)
    return new_item


def create_all_items(wavefiles, distance):
    "Create a string represeting all the files in project "
    position = 1
    items = ""
    for wavefile in wavefiles:
        items += create_item(wavefile, position)
        position += (wavefile.length_in_seconds +
                     distance * wavefile.length_in_seconds)

    return items


def create_track_with_items(items):  # items = string:
    track = create_empty_track()
    track = track[:-2] + items + track[-2:]
    return track


def create_project(track):
    with open('resources/reaper/skeleton.txt') as f:
        skeleton = f.read()
    project = skeleton[:-2] + track + skeleton[-2:]
    return project


def generate_reaper_project(wavefiles, distance):
    items = create_all_items(wavefiles, distance)
    track = create_track_with_items(items)
    project = create_project(track)
    return project
