import PySimpleGUI as sg
from session_creator import main
import os

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Select input file:')],
          [sg.Input(key='_input_file_',
           default_text='../tests/resources/input_files/file_list.xlsx'),
           sg.FileBrowse()],
          [sg.Text('Select spreadsheet range (for Excel files):')],
          [sg.T('Column:'),
           sg.I(default_text="C", size=(2, None), key='_column_'),
           sg.T('First Row:'),
           sg.I(default_text='5', size=(4, None), key='_firstrow_'),
           sg.T('Last Row:'),
           sg.I(default_text='8', size=(4, None), key='_lastrow_')],
          [sg.Text('Adjust distance between files (in multiples of length):'),
           sg.I(default_text='2', size=(3, None), key='_distance_')],
          [sg.Text('Select audio folder:')],
          [sg.Input(key='_folder_', 
           default_text='../tests/resources/test_audio'),
           sg.FolderBrowse()],
          [sg.Text('Select output file::')],
          [sg.Input(key='_output_file_',
           default_text='../tests/test_gui.RPP'),
          sg.FileSaveAs(
              file_types=(('ALL Files', '*.*'), ('Reaper project', '*.RPP')))],
          [sg.T(' '*40), sg.Button(button_text='Generate')]
          ] 

# Create the Window
window = sg.Window('DAW Session Creator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event, values)
    if event is None:
        break
    if event == 'Generate':
        target_dir, target_name = os.path.split(values['_output_file_'])
        list_file = values['_input_file_']
        directory = values['_folder_']
        distance_multiplier = float(values['_distance_'])  
        column = values['_column_']
        row_range = (int(values['_firstrow_']), int(values['_lastrow_']))

        main(list_file, target_dir, target_name, directory,
             distance_multiplier, column, row_range)

window.close()