import os
import settings as st


class UserInput():
    """Self-validating class containing all parameters give by the user"""

    def __init__(self, list_file_path="", output_file_path="",
                 audio_directory="", distance_multiplier=2, column="",
                 row_range=(None, None)):

        self.errors = []
        self.list_file_path, self.list_file_type = self.validate_list_file(
            list_file_path)
        self.output_file_path, self.output_file_type = \
            self.validate_output_file(output_file_path)
        self.audio_directory = self.validate_directory(audio_directory)
        self.distance_multiplier = \
            self.validate_distance_multiplier(distance_multiplier)
        if self.list_file_type == "spreadsheet":
            self.column, self.start_row, self.last_row = \
                self.validate_excel_range(column, row_range)

    def validate_list_file(self, list_file_path):

        if os.path.isfile(list_file_path):
            list_file_type = self.get_list_file_type(list_file_path)
        else:
            self.errors.append("Input file not found.")
            list_file_type = None

        return list_file_path, list_file_type

    def get_list_file_type(self, list_file_path):

        extension = os.path.splitext(list_file_path)[1].lower()
        if not any(extension in st.input_formats[ext_type]
                   for ext_type in st.input_formats):
            self.errors.append("Unknown input file type.")
            list_file_type = None
        else:
            for known_type in st.input_formats:
                for known_extension in st.input_formats[known_type]:
                    if extension == known_extension:
                        list_file_type = known_type

        return list_file_type

    def validate_output_file(self, output_file_path):

        if os.path.exists(os.path.split(output_file_path)[0]):
            output_file_type = self.validate_output_file_type(output_file_path)
            return output_file_path, output_file_type
        else:
            self.errors.append("Wrong output file path.")
            return None, None

    def validate_output_file_type(self, output_file_path):

        extension = os.path.splitext(output_file_path)[1].lower()
        if extension in st.output_formats.keys():
            return st.output_formats[extension]
        else:
            self.errors.append("Unsupported output file format.")
            return None

    def validate_directory(self, audio_directory):

        if os.path.exists(audio_directory):
            return audio_directory
        else:
            self.errors.append("Invalid audio directory path.")
            return None

    def validate_distance_multiplier(self, distance_multiplier):

        try:
            distance_multiplier = float(distance_multiplier)
        except ValueError:
            self.errors.append("Invalid distance value.")
        except TypeError:
            self.errors.append("Input error.")
        return distance_multiplier

    def validate_excel_range(self, column, row_range):

        try:
            if not column.isalpha():
                # check is column is a letter
                self.errors.append('Invalid column letter.')
        except AttributeError:
            self.errors.append("Column letter missing.")

        column = column.lower()

        try:  # check if start...
            row_start = int(row_range[0])
        except TypeError:
            self.errors.append("Start row missing")
            row_start = None
        except ValueError:
            self.errors.append("Start row invalid")
            row_start = None

        try:  # ...and stop rows are valid
            row_stop = int(row_range[1])
        except TypeError:
            self.errors.append("Stop row missing")
            row_stop = None
        except ValueError:
            self.errors.append("Stop row invalid")
            row_stop = None

        if row_start and row_stop:
            if row_stop < row_start:
                self.errors.append("Stop row larger than start row")

        return column, row_start, row_stop
