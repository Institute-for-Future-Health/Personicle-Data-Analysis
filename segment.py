import csv
import json
from collections import OrderedDict

from makeDataShared import makeDataShared


class segment:

    def __init__(self, data_path: str, name: str, date: str):
        self._data_path = data_path
        self._name = name
        self._date = date

    def get_segment(self) -> None:
        if 'lifelog' in self._data_path:
            path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/' + self._name + '_segment_restaurant.csv'
            total = self._get_labeled_home_event_with_going(self._data_path)
        else:
            path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/' + self._name + '_segment.csv'
            total = self._get_labeled_home_event_with_going(self._data_path)


        segment_total = self._segment(total)


        csvWrite = csv.writer(
            open(path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in segment_total:
            time = segment_total[key]['time']
            heartRate = segment_total[key]['heartRate']
            step = segment_total[key]['step']
            segmentType = segment_total[key]['segmentType']
            dailyActivity = segment_total[key]['dailyActivity']

            for counter in range(0, len(heartRate)):
                csvWrite.writerow([key, time[counter], heartRate[counter], step[counter], segmentType, dailyActivity])

    def get_segment_res(self, total: dict, path: str):
        segment_total = self._segment(total)

        csvWrite = csv.writer(
            open(path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in segment_total:
            time = segment_total[key]['time']
            heartRate = segment_total[key]['heartRate']
            step = segment_total[key]['step']
            segmentType = segment_total[key]['segmentType']
            dailyActivity = segment_total[key]['dailyActivity']

            for counter in range(0, len(heartRate)):
                csvWrite.writerow([key, time[counter], heartRate[counter], step[counter], segmentType, dailyActivity])

    def _segment(self, total: dict):
        segment = {}
        for key in total:
            timeWindow = int(key[10:])
            hour = int(timeWindow / 12)
            baseMinute = (timeWindow % 12) - 1

            if baseMinute < 0:
                hour -= 1
                baseMinute = 55
            else:
                baseMinute = baseMinute * 5

            heartRate = total[key]['heartRate']
            step = total[key]['step']
            if 'dailyActivity' not in total[key]:
                dailyActivity = 'dummy'
            else:
                dailyActivity = total[key]['dailyActivity']

            dataSet = {}
            heartRateArray = []
            timeArray = []
            stepArray = []
            prevSegmentType = ''
            segCounter = 0

            for counter in range(0, len(heartRate)):
                time = str(hour) + ':' + str(baseMinute)
                print(timeWindow,': ,', time,', ', heartRate[counter])
                baseMinute += 1
                if baseMinute >= 60:
                    baseMinute = 0
                    hour += 1

                if len(heartRate) <= len(step):
                    segmentType = makeDataShared.getSegmentType(step[counter])

                    if counter == 0:
                        heartRateArray.append(heartRate[counter])
                        timeArray.append(time)
                        stepArray.append(step[counter])

                        dataSet.update({'segmentType': segmentType})
                        dataSet.update({'heartRate': heartRateArray})
                        dataSet.update({'time': timeArray})
                        dataSet.update({'step': stepArray})
                        dataSet.update({'dailyActivity': dailyActivity})

                    else:
                        if segmentType == prevSegmentType:
                            heartRateArray.append(heartRate[counter])
                            timeArray.append(time)
                            stepArray.append(step[counter])

                            dataSet.update({'heartRate': heartRateArray})
                            dataSet.update({'time': timeArray})
                            dataSet.update({'step': stepArray})
                            dataSet.update({'dailyActivity': dailyActivity})

                            if counter == len(heartRate) - 1:
                                newSegCounter = '{0:03d}'.format(segCounter)
                                dickey = '{}{}{}'.format(key, '_', newSegCounter)
                                segCounter += 1
                                segment.update({dickey: dataSet})
                                dataSet = {}
                                heartRateArray = []
                                timeArray = []
                                stepArray = []
                        else:
                            if counter != len(
                                    heartRate) - 1 and prevSegmentType == 1 and segmentType == 0 and makeDataShared.getSegmentType(
                                    step[counter + 1]) == 1:
                                heartRateArray.append(heartRate[counter])
                                timeArray.append(time)
                                stepArray.append(step[counter])

                                segmentType = 1
                                dataSet.update({'heartRate': heartRateArray})
                                dataSet.update({'time': timeArray})
                                dataSet.update({'step': stepArray})
                                dataSet.update({'dailyActivity': dailyActivity})

                            else:
                                newSegCounter = '{0:03d}'.format(segCounter)
                                dickey = '{}{}{}'.format(key, '_', newSegCounter)
                                segCounter += 1
                                segment.update({dickey: dataSet})
                                dataSet = {}
                                heartRateArray = []
                                timeArray = []
                                stepArray = []

                                heartRateArray.append(heartRate[counter])
                                timeArray.append(time)
                                stepArray.append(step[counter])

                                dataSet.update({'segmentType': segmentType})
                                dataSet.update({'heartRate': heartRateArray})
                                dataSet.update({'time': timeArray})
                                dataSet.update({'step': stepArray})
                                dataSet.update({'dailyActivity': dailyActivity})

                    prevSegmentType = segmentType

        segment = OrderedDict(sorted(segment.items()))

        return makeDataShared._getFilteredSegment(makeDataShared, segment)

    def _get_labeled_home_event_with_going(self, path: str) -> dict:
        data = json.load(open(path))
        total = {}

        if 'segment' in data:
            data = data['segment']

            for date in data:
                object = data[date]
                for timeWindow in object:
                    if '2018' in date and timeWindow != None and isinstance(timeWindow, str):
                        segment = object[timeWindow]
                        if 'heartRate' in segment:
                            dailyActivity = segment['dailyActivitySet'][0]['KEY_DAILYACTIVITY']
                            segmentType = 0
                            dataSet = {}
                            if 'heartRate' in segment and 'step' in segment:
                                dataSet.update({'heartRate': segment['heartRate']})
                                dataSet.update({'step': segment['step']})
                                dataSet.update({'activtyLevel': segment['activtyLevel']})
                                dataSet.update({'segmentType': segmentType})
                                dataSet.update({'dailyActivity': dailyActivity})

                                timeWindow = '{0:03d}'.format(int(timeWindow))
                                key = '{}{}{}'.format(date, '_', timeWindow)

                                total[key] = dataSet
        else:
            for timeWindow in data:
                segment = data[timeWindow]
                if 'heartRate' in segment:
                    dailyActivity = segment['dailyActivitySet'][0]['KEY_DAILYACTIVITY']
                    segmentType = 0
                    dataSet = {}
                    if 'heartRate' in segment and 'step' in segment:
                        dataSet.update({'heartRate': segment['heartRate']})
                        dataSet.update({'step': segment['step']})
                        dataSet.update({'activtyLevel': segment['activtyLevel']})
                        dataSet.update({'segmentType': segmentType})
                        dataSet.update({'dailyActivity': dailyActivity})

                        timeWindow = '{0:03d}'.format(int(timeWindow))
                        key = '{}{}{}'.format(self._date, '_', timeWindow)

                        total[key] = dataSet




        return total
