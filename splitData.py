import csv


class splitData:
    def __init__(self, data_path: str, attributes: list, data_type: str):
        self._data_path = data_path
        self._data_type = data_type
        self._attributes = attributes

        self._get_data()

        self._split()

    def _get_data(self):
        self._data = {}

        with open(self._data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            for row in readCSV:
                time_window = row[0]

                if time_window not in self._data:
                    temp = {}
                    for count in range(1, len(self._attributes)):
                        if str(row[count]).isdigit():
                            temp.update({self._attributes[count]: [int(row[count])]})
                        elif self._attributes[count] == 'label' or self._attributes[count] == 'meal_type':
                            temp.update({self._attributes[count]: row[count]})
                        else:
                            temp.update({self._attributes[count]: [row[count]]})

                    self._data.update({time_window: temp})
                else:
                    temp = dict(self._data[time_window])
                    for count in range(1, len(self._attributes)):
                        if str(row[count]).isdigit():
                            temp_list = list(temp[self._attributes[count]])
                            temp_list.append(int(row[count]))
                            temp.update({self._attributes[count]: temp_list})
                        elif self._attributes[count] == 'label' or self._attributes[count] == 'meal_type':
                            temp.update({self._attributes[count]: row[count]})
                        else:
                            temp_list = list(temp[self._attributes[count]])
                            temp_list.append(row[count])
                            temp.update({self._attributes[count]: temp_list})

                    self._data.update({time_window: temp})

    def _split(self):
        # data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/dualSegment_res.csv'
        breakfast = {}
        lunch = {}
        dinner = {}
        dessert = {}

        for time_window in self._data:
            meal_type = self._data[time_window]['meal_type']
            if 'Breakfast' in meal_type:
                breakfast.update({time_window: self._data[time_window]})
            elif 'Lunch' in meal_type:
                lunch.update({time_window: self._data[time_window]})
            elif 'Dinner' in meal_type:
                dinner.update({time_window: self._data[time_window]})
            elif 'Desert' in meal_type:
                dessert.update({time_window: self._data[time_window]})
            elif 'Snack' in meal_type:
                dessert.update({time_window: self._data[time_window]})

        self._generate_csv(breakfast, 'breakfast')
        self._generate_csv(lunch, 'lunch')
        self._generate_csv(dinner, 'dinner')
        self._generate_csv(dessert, 'dessert')
        self._generate_csv(dessert, 'snack')

    def _generate_csv(self, data: dict, meal_type: str):
        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/split/'+meal_type+'_'+self._data_type+'.csv'

        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in data:
            attr_list = []
            for attr in data[key]:
                attr_list.append(data[key][attr])

            for counter in range(0, len(attr_list[0])):
                writing_list = [key]

                for newCounter in attr_list:
                    if type(newCounter) == list:
                        writing_list.append(newCounter[counter])
                    else:
                        writing_list.append(newCounter)

                csvWrite.writerow(writing_list)
