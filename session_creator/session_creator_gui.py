import PySimpleGUI as sg
from session_creator import main, get_files
from process import create_wavefile_objects
import settings as st
from user_input import UserInput
import string

# Create GUI:
sg.theme('DarkAmber')   # Add a touch of color

audio_table = sg.Table([[" " for col in range(3)] for row in range(10)],
    headings=["Filename", "Bitrate", "Samplerate", "Channels"], size=(54, 10),
    num_rows=10, col_widths=[22, 6, 9, 8], auto_size_columns=False, 
    key="_wav_data_display_", justification='left')

layout = [
    # Row 1 - text
    [sg.Text('Select input file:', size=(55, 1), justification='center'), 
     sg.VSep(),
     sg.Text('Select audio folder:', size=(55, 1), justification='center')],
    # Row 2 - file input
    [sg.Input(key='_input_file_',default_text=st.gui_default_input_path),
     sg.FileBrowse(), sg.VSep(), 
     sg.Input(key='_folder_', default_text=st.gui_default_audio_folder),
     sg.FolderBrowse()],
    # Row 3 - range
    [sg.Text(" "*20), sg.Text('Select spreadsheet range (for Excel files):')],
    [sg.T(" "*10), sg.T('Column:'),
     sg.I(default_text="C", size=(2, None), key='_column_', 
             enable_events=True),
     sg.T('First Row:'),
     sg.I(default_text='5', size=(4, None), key='_firstrow_',
             enable_events=True),
     sg.T('Last Row:'),
     sg.I(default_text='8', size=(4, None), key='_lastrow_',
            enable_events=True)],
    # Row 4 - file display
    [sg.Listbox(values="", size=(54, 10), key="_file_list_"), 
     sg.VerticalSeparator(), 
     audio_table],
    # Row 5 - Distance and output file
    [sg.Text('Distance between files (in multiples of length):'),
     sg.I(default_text='2', size=(3, None), key='_distance_'),  sg.Text(" "*22),
     sg.Text('Output file:'),
     sg.Input(key='_output_file_', size=(30, 1),
    default_text=st.gui_default_output_path),
     sg.FileSaveAs(
        file_types=(('ALL Files', '*.*'), ('Reaper project', '*.RPP')))],
    # Row 6 - Generate
    [sg.T("", size=(45, 1)), sg.B(button_text='Check'), 
     sg.B(button_text='Generate')]
    ]

def read_data():
    list_file_path = values['_input_file_']
    output_file_path = values['_output_file_']
    directory = values['_folder_']
    distance_multiplier = values['_distance_']
    column = values['_column_']
    row_range = (values['_firstrow_'], values['_lastrow_'])

    user_input = UserInput(list_file_path, output_file_path, directory,
                        distance_multiplier, column, row_range)

    return user_input


# Create the Window
window = sg.Window('DAW Session Creator', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # print(event, values)
    if event is None:
        break

    if (event == ('_column_') and values['_column_'] and 
                     values['_column_'][-1] not in string.ascii_letters):
        window['_column_'].update(values['_column_'][:-1])

    if (event in ('_firstrow_', '_lastrow_') and values[event] and
                    values[event][-1] not in string.digits):
        window[event].update(values[event][:-1])

    if event == 'Check':
        user_input = read_data()
        files_to_load, wav_files, good_files = get_files(user_input)
        wave_data = create_wavefile_objects(wav_files, wav_files, 
                                            user_input.audio_directory)
        wav_data = [[wav.filename, wav.bitrate, wav.samplerate, wav.nchannels] 
                     for wav in wave_data]

        window['_file_list_'].update(files_to_load)
        window['_wav_data_display_'].update(wav_data)
        
    if event == 'Generate':
        user_input = read_data()
        

        if user_input.errors:
            print(f"User input: {user_input.errors}")

        else:
            main(user_input)

window.close()
