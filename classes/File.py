from collections import namedtuple


class File:
    def __init__(self, filename):
        self.filename = self.__set_attribute(filename)

    def __set_attribute(self, attribute):
        if not isinstance(attribute, str):
            warning_phase = "ERROR: '{}' should be a string"
            self.__raise_error(TypeError, warning_phase, attribute)
        elif len(attribute) == 0:
            warning_phase = "ERROR: '{}' shouldn't have length equal zero"
            self.__raise_error(ValueError, warning_phase, attribute)
        else:
            return attribute

    def __raise_error(self, error_function, warning_phase, key_word):
        raise error_function(warning_phase.format(key_word))

    def get_data_from_file(self):
        data = self.__read_file()
        data = self.__clean_list(data)
        if self.__is_list_empty(data):
            raise TypeError('ERROR: list of email cannot be empty')
        return data
    
    def __is_list_empty(self, some_list):
        return len(some_list) == 0

    def __read_file(self):
        with open(self.filename) as file:
            file_data = []
            line = file.readline()

            while line:
                file_data.append(str(line).strip('\n'))
                line = file.readline()

            file.close()
        return file_data

    def __clean_list(self, file_data):
        clean_list = [
            line for line in file_data
            if isinstance(line, str) and len(line) != 0
        ]
        return clean_list

    def get_content_as_list_of_class(self):
        Domain = namedtuple('Domain', ['name', 'owner'])
        domains = self.__read_file()
        domains = self.__clean_list(domains)
        if self.__is_list_empty(domains):
            raise TypeError('ERROR: list of domains cannot be empty')
        result = [Domain(line.split('=')[0], line.split('=')[1])
                  for line in domains]

        return result
