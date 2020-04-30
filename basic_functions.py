def write_filenames(files):
    """Only for creating list for development"""
    with open('list_of_files.txt', 'w') as f:
        for name_of_wav in files:
            f.write(name_of_wav + '\n')
