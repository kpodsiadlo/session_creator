import string
from openpyxl import load_workbook


def get_filenames_from_excel_column(
        filename, column_letter, row_start_num, row_stop_num):
    """Return a list of entries in a given column"""

    column_letter_lowercase = column_letter.lower()
    column_number = int(ord(column_letter_lowercase) - 96)
    # get the file
    wb = load_workbook(filename)
    # get the sheet
    ws = wb['Sheet1']
    # get the values
    file_list = [ws.cell(row=i, column=column_number).value
                 for i in range(row_start_num, row_stop_num+1)]

    return file_list
