
class ValuesTxtFile:

    def __init__(self, file_path):

        self.__file = open(file_path)
        self.__file_lines_list = None

    def get_file_lines_list(self):
        if self.__file_lines_list is None:
            self.__generate_file_lines_list()
        return self.__file_lines_list

    def __generate_file_lines_list(self):
        content = self.__file.readlines()
        content = [x.strip() for x in content]  # remove '/n' at the end of the lines
        self.__file_lines_list = content

    def get_value_by_key(self, key):

        ''' Value must be one line under the key line for function to work
            If a key is not found, the function will raise an error. '''

        # search for key line
        try:
            key_line_index = self.get_file_lines_list().index(key)

        # if key not found
        except ValueError:
            raise ValueError('Key is not found in the file')

        # calculate value and return
        value_line_index = key_line_index + 1
        try:
            return self.get_file_lines_list()[value_line_index]

        # if the key is the last line
        except IndexError:
            raise ValueError('Key is the last line in the file')
