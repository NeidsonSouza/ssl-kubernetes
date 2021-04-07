import csv


class Domains:
    def __init__(self, csv_file):
        self._domains = self.__get_domains(csv_file)
        
    def __get_domains(self, csv_file):
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return tuple(dict(row) for row in reader)
        
    def __len__(self):
        return len(self._domains)

    def __getitem__(self, index):
        return self._domains[index]
        