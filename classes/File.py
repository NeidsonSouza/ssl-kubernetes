from collections import namedtuple

class File:
    def __init__(self, file_name):
        self.file_name = file_name


    def read_file(self):
        with open(self.file_name) as file:
            file_data = []
            line = file.readline()

            while line:
                file_data.append(str(line).strip('\n'))
                line = file.readline()
            
            file.close()
        
        return file_data

    
    def get_content_as_list(self):
        Domain = namedtuple('Domain', ['name', 'owner'])
        lines = self.read_file()
        result = [Domain(line.split('=')[0], line.split('=')[1]) for line in lines]
        
        return result
