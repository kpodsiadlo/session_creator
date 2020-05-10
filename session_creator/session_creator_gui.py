import PySimpleGUI as sg
from session_creator import main
import settings as st
from user_input import UserInput
import string

# Create GUI:
sg.theme('DarkAmber')   # Add a touch of color
layout = [[sg.Text('Select input file:')],
          [sg.Input(key='_input_file_',
           default_text=st.gui_default_input_path),
           sg.FileBrowse()],
          [sg.Text('Select spreadsheet range (for Excel files):')],
          [sg.T('Column:'),
           sg.I(default_text="C", size=(2, None), key='_column_', 
           enable_events=True),
           sg.T('First Row:'),
           sg.I(default_text='5', size=(4, None), key='_firstrow_',
           enable_events=True),
           sg.T('Last Row:'),
           sg.I(default_text='8', size=(4, None), key='_lastrow_',
           enable_events=True)],
          [sg.Text('Adjust distance between files (in multiples of length):'),
           sg.I(default_text='2', size=(3, None), key='_distance_')],
          [sg.Text('Select audio folder:')],
          [sg.Input(key='_folder_',
           default_text=st.gui_default_audio_folder),
           sg.FolderBrowse()],
          [sg.Text('Select output file::')],
          [sg.Input(key='_output_file_',
           default_text=st.gui_default_output_path),
          sg.FileSaveAs(
              file_types=(('ALL Files', '*.*'), ('Reaper project', '*.RPP')))],
          [sg.T(' '*25), sg.B(button_text='Check files'), 
           sg.B(button_text='Generate')]
          ]

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


    if event == 'Generate':
        # Get data from the user input
        list_file_path = values['_input_file_']
        output_file_path = values['_output_file_']
        directory = values['_folder_']
        distance_multiplier = values['_distance_']
        column = values['_column_']
        row_range = (values['_firstrow_'], values['_lastrow_'])

        user_input = UserInput(list_file_path, output_file_path, directory,
                           distance_multiplier, column, row_range)

        if user_input.errors:
            print(f"User input: {user_input.errors}")

        else:
            main(user_input)

window.close()
