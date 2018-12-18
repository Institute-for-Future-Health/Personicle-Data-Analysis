import csv


class noiseFilter:
    def __init__(self, data_path: str):
        self._data_path = data_path

    def _time_cleaning(self):
        with open(self._data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            for row in readCSV:
                row[0]
