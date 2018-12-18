import csv
import datetime

from makeDataShared import makeDataShared
from variable import variable


class dualSegment:
    def __init__(self, data_path: str, attributes: list, data_type: int, user_name: str):
        self._user_name = user_name
        self._data_path = data_path
        self._attributes = attributes
        self._data_type = data_type

        self._get_data()

        if data_type == variable.restaurant:
            self._get_dual_segment_result()

        self._add_SAX_heart_rate()
        self._generate_csv()
        print('done')

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
                        elif self._attributes[count] == 'label':
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
                        elif self._attributes[count] == 'label':
                            temp.update({self._attributes[count]: row[count]})
                        else:
                            temp_list = list(temp[self._attributes[count]])
                            temp_list.append(row[count])
                            temp.update({self._attributes[count]: temp_list})

                    self._data.update({time_window: temp})

    def _get_dual_segment_result(self):
        dual_segment_data = {}
        for value in self._data:
            segCounter = 0
            dataSet = {}
            list_attribute = []
            for count in range(0, len(self._attributes) - 1):
                list_temp = []
                list_attribute.append(list_temp)

            for counter in range(0, len(self._data[value]['step'])):
                segmentType = makeDataShared.getSegmentType(self._data[value]['step'][counter])

                if counter == 0:
                    for count in range(1, len(self._attributes)):
                        if self._attributes[count] != 'label' and self._attributes[count] != 'meal_type':
                            if type(self._data[value][self._attributes[count]]) == list:
                                list_attribute[count - 1].append(self._data[value][self._attributes[count]][counter])
                            else:
                                list_attribute[count - 1].append(self._data[value][self._attributes[count]])

                            dataSet.update({self._attributes[count]: list_attribute[count - 1]})

                    dataSet.update({'segmentType': segmentType})
                    dataSet.update({'meal_type': self._data[value]['meal_type'][0]})
                    dataSet.update({'label': self._data[value]['label']})
                else:
                    if segmentType == prevSegmentType:
                        for count in range(1, len(self._attributes)):
                            if self._attributes[count] != 'label' and self._attributes[count] != 'meal_type':
                                if type(self._data[value][self._attributes[count]]) == list:
                                    list_attribute[count - 1].append(
                                        self._data[value][self._attributes[count]][counter])
                                else:
                                    list_attribute[count - 1].append(self._data[value][self._attributes[count]])

                                dataSet.update({self._attributes[count]: list_attribute[count - 1]})

                        # for count in range(1, len(self._attributes) - 1):
                        #     list_attribute[count - 1].append(self._data[value][self._attributes[count]][counter])
                        #     dataSet.update({self._attributes[count]: list_attribute[count - 1]})

                        if counter == len(self._data[value]['heart_rate']) - 1:
                            newSegCounter = '{0:03d}'.format(segCounter)
                            dickey = '{}{}{}'.format(value, '_', newSegCounter)
                            segCounter += 1
                            dual_segment_data.update({dickey: dataSet})
                            dataSet = {}
                            list_attribute = []
                            for count in range(0, len(self._attributes) - 1):
                                list_temp = []
                                list_attribute.append(list_temp)
                    else:
                        if counter != len(self._data[value]['heart_rate']) - 1 and prevSegmentType == 1 \
                                and segmentType == 0 \
                                and makeDataShared.getSegmentType(self._data[value]['step'][counter + 1]) == 1:

                            # for count in range(1, len(self._attributes) - 1):
                            #     list_attribute[count - 1].append(self._data[value][self._attributes[count]][counter])
                            #     dataSet.update({self._attributes[count]: list_attribute[count - 1]})
                            for count in range(1, len(self._attributes)):
                                if self._attributes[count] != 'label' and self._attributes[count] != 'meal_type':
                                    if type(self._data[value][self._attributes[count]]) == list:
                                        list_attribute[count - 1].append(
                                            self._data[value][self._attributes[count]][counter])
                                    else:
                                        list_attribute[count - 1].append(self._data[value][self._attributes[count]])

                                    dataSet.update({self._attributes[count]: list_attribute[count - 1]})


                            segmentType = 1

                        else:
                            newSegCounter = '{0:03d}'.format(segCounter)
                            dickey = '{}{}{}'.format(value, '_', newSegCounter)
                            segCounter += 1
                            dual_segment_data.update({dickey: dataSet})
                            dataSet = {}
                            list_attribute = []
                            for count in range(0, len(self._attributes) - 1):
                                list_temp = []
                                list_attribute.append(list_temp)

                            for count in range(1, len(self._attributes)):
                                if self._attributes[count] != 'label' and self._attributes[count] != 'meal_type':
                                    if type(self._data[value][self._attributes[count]]) == list:
                                        list_attribute[count - 1].append(
                                            self._data[value][self._attributes[count]][counter])
                                    else:
                                        list_attribute[count - 1].append(self._data[value][self._attributes[count]])

                                    dataSet.update({self._attributes[count]: list_attribute[count - 1]})

                            dataSet.update({'segmentType': segmentType})
                            dataSet.update({'meal_type': self._data[value]['meal_type'][0]})
                            dataSet.update({'label': self._data[value]['label']})

                            # for count in range(1, len(self._attributes) - 1):
                            #     list_attribute[count - 1].append(self._data[value][self._attributes[count]][counter])
                            #     dataSet.update({self._attributes[count]: list_attribute[count - 1]})
                            #
                            # dataSet.update({'segmentType': segmentType})
                            # dataSet.update({'label': self._data[value][self._attributes[len(self._attributes) - 1]]})

                prevSegmentType = segmentType
        self._data = dual_segment_data

    def _add_SAX_heart_rate(self):
        mean = 59.20210123326904
        std = 18.44932531139424

        for time_window in self._data:
            heart_rate = self._data[time_window]['heart_rate']
            # while heart_rate.count(0) > 0:
            #     heart_rate.remove(0)

            symbolic_heart_rate = []
            for hr in heart_rate:
                if hr == 0:
                    symbolic_heart_rate.append(0)
                else:
                    paa = (hr - mean) / std
                    symbolic_heart_rate.append(makeDataShared.convert_symbolic(paa))

            self._data[time_window].update({'symbolic_heart_rate': symbolic_heart_rate})

    def _generate_csv(self):
        if self._data_type == variable.restaurant:
            data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/'+self._user_name+'_segment_res.csv'
        elif self._data_type == variable.home:
            data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/dualSegment_home.csv'

        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in self._data:
            attr_list = []
            for attr in self._data[key]:
                attr_list.append(self._data[key][attr])

            # hour = int(int(key[10:13]) / 12)
            # if int(key[10:13]) % 12 == 0:
            #     min = 55
            # else:
            #     min = ((int(key[10:13]) % 12) - 1) * 5
            #
            # attr_list[0] = self._get_new_time_list(hour, min, len(attr_list[0]))

            for counter in range(0, len(attr_list[0])):
                writing_list = [key]

                for newCounter in attr_list:
                    if type(newCounter) == list:
                        writing_list.append(newCounter[counter])
                    else:
                        writing_list.append(newCounter)

                csvWrite.writerow(writing_list)

    def _get_new_time_list(self, start_hour: str, start_min: str, length: int) -> list:
        new_time_list = []
        hour = start_hour
        min = start_min
        for count in range(0, length):
            new_time = datetime.datetime(2018, 8, 6, int(hour), int(min)) + datetime.timedelta(
                minutes=int(count))
            new_time = "%s:%s" % (new_time.hour, new_time.minute)
            new_time_list.append(new_time)

        return new_time_list
