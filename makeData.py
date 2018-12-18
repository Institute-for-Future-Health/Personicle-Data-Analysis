import csv
import json
import statistics
from collections import OrderedDict
from makeDataShared import makeDataShared

import alphabet
import paa
import sax
import znorm
import numpy as np
import math

import numbers
import matplotlib.pyplot as plt


class makeData:
    pooya_skip = ['0407_2018', '0412_2018', '0413_2018', '0414_2018', '0422_2018', '0428_2018', '0505_2018',
                  '0506_2018', '0512_20182', '0514_2018']
    ramesh_skip = ['0409_2018', '0410_2018', '0416_2018', '0422_2018', '0423_2018', '0424_2018', '0425_2018',
                   '0426_2018', '0427_2018', '0430_2018', '0502_2018', '0506_2018']
    jordan_skip = ['0531_2018']

    minDuration = 5

    def __init__(self, segmentPath: str, symbolicDataPath: str, timeType: str, name: str):

        self._segmentPath = segmentPath
        self._symbolicDataPath = symbolicDataPath

        self._segmentData = json.load(open(self._segmentPath))
        self._segmentSize = []

        if name == 'Ramesh':
            newSegmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-Ramesh-0515-2018.json'
            newTotal = json.load(open(newSegmentPath))
            for value in self._segmentData:
                newTotal.update({value: self._segmentData[value]})

            self._segmentData = newTotal

        self._timeType = timeType
        self._name = name
        return

    def _hrAverage(self, total: dict, valueType: str):
        dataSet = {}
        mCount = 0
        mDelta = 0
        mAvg = 0
        mM2 = 0
        mStv = 0

        for counter in range(0, 24):
            dataSet.update({str(counter): []})

        # mCount = mCount + 1
        # mDelta = heartRateValue - mAvg
        # mAvg = mAvg + mDelta / mCount
        # mM2 = mM2 + mDelta * (heartRateValue - mAvg)
        # mStv = math.sqrt(mM2 / mCount)
        #
        for key in total:
            segmentType = total[key]['segmentType']
            time = total[key]['time']
            if valueType == 'real':
                heartRate = total[key]['heartRate']
            else:
                heartRate = total[key]['symbol']

            if segmentType == 0:
                for counter in range(0, len(time)):
                    if int(heartRate[counter]) != 0:
                        hour = time[counter][0:time[counter].rfind(':')]

                        # if int(hour) == 23:
                        #     mCount = mCount + 1
                        #     mDelta = int(heartRate[counter]) - mAvg
                        #     mAvg = mAvg + mDelta / mCount
                        #     mM2 = mM2 + mDelta * (int(heartRate[counter]) - mAvg)
                        #     mStv = math.sqrt(mM2 / mCount)

                        subset = dataSet[hour]
                        subset.append(int(heartRate[counter]))
                        dataSet.update({hour: subset})

        dataSet = OrderedDict(sorted(dataSet.items()))

        totalDataSet = {}

        for key in dataSet:
            if len(dataSet[key]) > 0:
                avg = statistics.mean(dataSet[key])
                std = statistics.stdev(dataSet[key])
                totalDataSet.update({int(key): {'avg': avg, 'std': std}})
            else:
                totalDataSet.update({int(key): {'avg': 0, 'std': 0}})

        return totalDataSet

    def _getCsv(self):
        with open('/Users/hyungiko/Desktop/Personicle Data/' + self._symbolicDataPath + '.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            prevKey = ''
            timeType = ''
            segmentType = ''
            label = ''
            dataSet = {}
            timeList = []
            symbolList = []
            stepList = []
            heartRateList = []

            for row in readCSV:
                currentKey = row[0]
                time = row[1]
                heartRate = int(row[2])
                timeBand = int(time[0:time.rfind(':')])
                if prevKey == '':
                    timeList.append(time)
                    stepList.append(int(row[3]))
                    symbolList.append(int(row[4]))
                    heartRateList.append(heartRate)
                    # print(currentKey)
                    label = int(row[7])
                    print(row[6])
                    segmentType = int(row[5])

                    if timeBand >= 17 and timeBand < 24:
                        timeType = 'evening'
                    elif timeBand > 11 and timeBand < 17:
                        timeType = 'afternoon'
                    elif timeBand >= 6 and timeBand <= 11:
                        timeType = 'morning'

                elif prevKey == currentKey:
                    timeList.append(time)
                    symbolList.append(int(row[4]))
                    stepList.append(int(row[3]))
                    heartRateList.append(heartRate)
                elif prevKey != currentKey:
                    subDataSet = {}
                    subDataSet.update({'time': timeList})
                    subDataSet.update({'symbol': symbolList})
                    subDataSet.update({'step': stepList})
                    subDataSet.update({'heartRate': heartRateList})
                    subDataSet.update({'label': label})
                    subDataSet.update({'timeType': timeType})
                    subDataSet.update({'segmentType': segmentType})
                    dataSet.update({prevKey: subDataSet})

                    timeList = []
                    symbolList = []
                    stepList = []
                    heartRateList = []
                    timeType = ''

                    timeList.append(time)
                    symbolList.append(int(row[4]))
                    stepList.append(int(row[3]))
                    heartRateList.append(heartRate)
                    label = int(row[7])
                    segmentType = int(row[5])

                    if timeBand >= 17 and timeBand < 24:
                        timeType = 'evening'
                    elif timeBand > 11 and timeBand < 17:
                        timeType = 'afternoon'
                    elif timeBand >= 6 and timeBand <= 11:
                        timeType = 'morning'

                prevKey = currentKey

        dataSet = OrderedDict(sorted(dataSet.items()))

        return dataSet

    def getTotalCsv(self, timeType: str, isNorm: bool):
        # with open('/Users/hyungiko/Desktop/Personicle Data/sampleSet_'+timeType+'_HR_withPrevNMseg_symbol.csv') as csvfile:
        # readCSV = csv.reader(csvfile, delimiter=',')
        # path = '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/normalized' + timeType + 'Result.csv'
        path = '/Users/hyungiko/Desktop/Personicle Data/Train/eveningTrain_20m_Jordan.csv'


        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            row_0 = []
            row_1 = []
            row_2 = []
            row_3 = []
            row_4 = []
            row_5 = []
            row_6 = []
            row_7 = []
            row_8 = []
            row_9 = []
            for row in readCSV:
                row_0.append(row[0])
                row_1.append(float(row[1]))
                row_2.append(float(row[2]))
                row_3.append(float(row[3]))
                row_4.append(float(row[4]))
                row_5.append(float(row[5]))
                row_6.append(float(row[6]))
                row_7.append(float(row[7]))
                row_8.append(float(row[8]))
                row_9.append(int(row[9]))

            row_1_avg = statistics.mean(row_1)
            row_2_avg = statistics.mean(row_2)
            row_3_avg = statistics.mean(row_3)
            row_4_avg = statistics.mean(row_4)
            row_5_avg = statistics.mean(row_5)
            row_6_avg = statistics.mean(row_6)
            row_7_avg = statistics.mean(row_7)
            row_8_avg = statistics.mean(row_8)

            row_1_std = statistics.stdev(row_1)
            row_2_std = statistics.stdev(row_2)
            row_3_std = statistics.stdev(row_3)
            row_4_std = statistics.stdev(row_4)
            row_5_std = statistics.stdev(row_5)
            row_6_std = statistics.stdev(row_6)
            row_7_std = statistics.stdev(row_7)
            row_8_std = statistics.stdev(row_8)

            total = []
            for i in range(0, len(row_1)):
                subTotal = []
                subTotal.append(row_0[i])
                if isNorm:
                    subTotal.append((row_1[i] - row_1_avg) / row_1_std)
                    subTotal.append((row_2[i] - row_2_avg) / row_2_std)
                    subTotal.append((row_3[i] - row_3_avg) / row_3_std)
                    subTotal.append((row_4[i] - row_4_avg) / row_4_std)
                    subTotal.append((row_5[i] - row_5_avg) / row_5_std)
                    subTotal.append((row_6[i] - row_6_avg) / row_6_std)
                    subTotal.append((row_7[i] - row_7_avg) / row_7_std)
                    subTotal.append((row_8[i] - row_8_avg) / row_8_std)
                else:
                    subTotal.append(row_1[i])
                    subTotal.append(row_2[i])
                    subTotal.append(row_3[i])
                    subTotal.append(row_4[i])
                    subTotal.append(row_5[i])
                    subTotal.append(row_6[i])
                    subTotal.append(row_7[i])
                    subTotal.append(row_8[i])

                subTotal.append(row_9[i])
                total.append(subTotal)
        return total

    def getTotalTestCsv(self, timeType: str, isNorm: bool):
        # with open('/Users/hyungiko/Desktop/Personicle Data/sampleSet_'+timeType+'_HR_withPrevNMseg_symbol.csv') as csvfile:
        # readCSV = csv.reader(csvfile, delimiter=',')
        # path = '/Users/hyungiko/Desktop/Personicle Data/Test/' + timeType + 'Test.csv'
        path = '/Users/hyungiko/Desktop/Personicle Data/Test/eveningTest_20m_jordan.csv'

        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            row_0 = []
            row_1 = []
            row_2 = []
            row_3 = []
            row_4 = []
            row_5 = []
            row_6 = []
            row_7 = []
            row_8 = []
            row_9 = []
            for row in readCSV:
                row_0.append(row[0])
                row_1.append(float(row[1]))
                row_2.append(float(row[2]))
                row_3.append(float(row[3]))
                row_4.append(float(row[4]))
                row_5.append(float(row[5]))
                row_6.append(float(row[6]))
                row_7.append(float(row[7]))
                row_8.append(float(row[8]))
                row_9.append(int(row[9]))

            row_1_avg = statistics.mean(row_1)
            row_2_avg = statistics.mean(row_2)
            row_3_avg = statistics.mean(row_3)
            row_4_avg = statistics.mean(row_4)
            row_5_avg = statistics.mean(row_5)
            row_6_avg = statistics.mean(row_6)
            row_7_avg = statistics.mean(row_7)
            row_8_avg = statistics.mean(row_8)

            row_1_std = statistics.stdev(row_1)
            row_2_std = statistics.stdev(row_2)
            row_3_std = statistics.stdev(row_3)
            row_4_std = statistics.stdev(row_4)
            row_5_std = statistics.stdev(row_5)
            row_6_std = statistics.stdev(row_6)
            row_7_std = statistics.stdev(row_7)
            row_8_std = statistics.stdev(row_8)

            total = []
            for i in range(0, len(row_1)):
                subTotal = []
                subTotal.append(row_0[i])
                if isNorm:
                    subTotal.append((row_1[i] - row_1_avg) / row_1_std)
                    subTotal.append((row_2[i] - row_2_avg) / row_2_std)
                    subTotal.append((row_3[i] - row_3_avg) / row_3_std)
                    subTotal.append((row_4[i] - row_4_avg) / row_4_std)
                    subTotal.append((row_5[i] - row_5_avg) / row_5_std)
                    subTotal.append((row_6[i] - row_6_avg) / row_6_std)
                    subTotal.append((row_7[i] - row_7_avg) / row_7_std)
                    subTotal.append((row_8[i] - row_8_avg) / row_8_std)
                else:
                    subTotal.append(row_1[i])
                    subTotal.append(row_2[i])
                    subTotal.append(row_3[i])
                    subTotal.append(row_4[i])
                    subTotal.append(row_5[i])
                    subTotal.append(row_6[i])
                    subTotal.append(row_7[i])
                    subTotal.append(row_8[i])

                subTotal.append(row_9[i])
                total.append(subTotal)
        return total

    def getTotalTrainCsv(self, timeType: str, interval: int, name: str):
        path = '/Users/hyungiko/Desktop/Personicle Data/Train/' + timeType + 'Train_' + str(
            interval) + 'm_' + name + '.csv'

        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            total = []
            for row in readCSV:
                subTotal = []

                subTotal.append(row[0])
                subTotal.append(float(row[1]))
                subTotal.append(float(row[2]))
                subTotal.append(float(row[3]))
                subTotal.append(float(row[4]))
                subTotal.append(float(row[5]))
                subTotal.append(float(row[6]))
                subTotal.append(float(row[7]))
                subTotal.append(float(row[8]))

                subTotal.append(int(row[9]))
                total.append(subTotal)

        return total

    def buildSymbolicResultCsv(self):
        self._buildSymbolicResultCsv('evening')
        self._buildSymbolicResultCsv('morning')
        self._buildSymbolicResultCsv('afternoon')

    def _buildSymbolicResultCsv(self, timeType: str):
        with open(
                '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/sampleSet_' + timeType + '.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            key = []
            prevPrevHr = []
            currHr = []
            hrDiff = []
            prevNMTime = []
            prevMTime = []
            prevMStep = []
            prepTime = []
            slope = []
            label = []

            for row in readCSV:
                key.append(row[0])

                if row[0] == '0524_2018_221_012':
                    test = float(row[4])
                    print(float(row[4]))

                prevPrevHr.append(float(row[1]))
                currHr.append(float(row[2]))
                hrDiff.append(float(row[3]))
                prevNMTime.append(float(row[4]))
                prevMTime.append(float(row[5]))
                prevMStep.append(float(row[6]))
                prepTime.append(float(row[7]))
                slope.append(float(row[8]))
                label.append(row[9])

            threshold = len(key)
            # if 'Jordan' in self._segmentPath:
            #     with open('/Users/hyungiko/Desktop/Personicle Data/'+self._name+'/merged/sampleSet_' + timeType + '_merged.csv') as csvfile:
            #         readCSV2 = csv.reader(csvfile, delimiter=',')
            #         key = []
            #         prevNMTime = []
            #         prevMTime = []
            #         prevMStep = []
            #         for row in readCSV2:
            #             key.append(row[0])
            #             prevNMTime.append(float(row[4]))
            #             prevMTime.append(float(row[5]))
            #             prevMStep.append(float(row[6]))

            prevMStep_list = prevMStep
            for i in range(0, len(prevMStep_list)):
                if prevMStep_list[i] == 0:
                    prevMStep_list[i] = 1
                elif prevMStep_list[i] > 150:
                    prevMStep_list[i] = 150

            sd_prevMStep = np.std(np.array(prevMStep_list))
            mean_prevMStep = np.mean(np.array(prevMStep_list))

            prevNMTime_list = prevNMTime
            for i in range(0, len(prevNMTime_list)):
                if prevNMTime_list[i] == 0:
                    prevNMTime_list[i] = 1
                elif prevNMTime_list[i] > 100:
                    prevNMTime_list[i] = 100

            sd_prevNMTime = np.std(np.array(prevNMTime_list))
            mean_prevNMTime = np.mean(np.array(prevNMTime_list))

            mCount = 0
            mDelta = 0
            mAvg = 0
            mStv = 0
            mM2 = 0

            for i in range(0, len(prevMStep_list)):
                mCount = mCount + 1
                mDelta = float(prevMStep_list[i]) - mAvg
                mAvg = mAvg + mDelta / mCount
                mM2 = mM2 + mDelta * (float(prevMStep_list[i]) - mAvg)
                mStv = math.sqrt(mM2 / mCount)

            print('timeType1: ', timeType, 'mStv:', sd_prevMStep, ', mAvg: ', mean_prevMStep)
            print('timeType2: ', timeType, 'mStv:', mStv, ', mAvg: ', mAvg, 'mCount: ', mCount, ', mM2: ', mM2)
            # print('prevMTime_list: ', float(prevNMTime_list[0]))

            # for i in range(0, len(prevMTime)):
            #
            #     mCount = mCount + 1
            #     mDelta = float(prevMTime[i]) - mAvg
            #     mAvg = mAvg + mDelta / mCount
            #     mM2 = mM2 + mDelta * (float(prevMTime[i]) - mAvg)
            #     mStv = math.sqrt(mM2 / mCount)

            # for i in range(0, len(prevNMTime_list)):
            #
            #     mCount = mCount + 1
            #     mDelta = float(prevNMTime_list[i]) - mAvg
            #     mAvg = mAvg + mDelta / mCount
            #     mM2 = mM2 + mDelta * (float(prevNMTime_list[i]) - mAvg)
            #     mStv = math.sqrt(mM2 / mCount)

            prevMTime_list = prevMTime

            sd_prevMTime = np.std(np.array(prevMTime_list))
            mean_prevMTime = np.mean(np.array(prevMTime_list))

            csvWrite = csv.writer(
                open(
                    '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/normalized' + timeType + 'Result.csv',
                    'w'),
                delimiter=',', quotechar='|',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for i in range(0, len(prevPrevHr)):
                subTotal = []
                subTotal.append(key[i])
                subTotal.append(prevPrevHr[i])
                subTotal.append(currHr[i])
                subTotal.append(hrDiff[i])

                subTotal.append(self._getSymbolicValue(prevNMTime[i], 4, sd_prevNMTime, mean_prevNMTime))
                subTotal.append(self._getSymbolicValue(prevMTime[i], 3, sd_prevMTime, mean_prevMTime))
                subTotal.append(self._getSymbolicValue(prevMStep[i], 5, sd_prevMStep, mean_prevMStep))

                # print(key[i], ',', self._getSymbolicValue(prevNMTime[i], 4, sd_prevNMTime, mean_prevNMTime))

                # subTotal.append(prevNMTime[i])
                # subTotal.append(prevMTime[i])
                # subTotal.append(prevMStep[i])

                subTotal.append(prepTime[i])
                subTotal.append(slope[i])
                subTotal.append(label[i])
                # subTotal.append(slope10[i])

                csvWrite.writerow(subTotal)
                # total.append(subTotal)

        # return total

    def get_segment_size(self) -> list:
        return self._segmentSize

    def _addPrevPrevSegment(self, timeType: str):
        dataSet = self._getCsv()
        hrAvgSymbol = self._hrAverage(dataSet, 'symbol')
        hrAvgReal = self._hrAverage(dataSet, 'real')

        for key in dataSet:
            if 0 in dataSet[key]['heartRate']:
                dataSet[key]['heartRate'] = [x for x in dataSet[key]['heartRate'] if x != 0]
                dataSet[key]['symbol'] = [x for x in dataSet[key]['symbol'] if x != 0]

        dataSet[key]['heartRate'] = [x for x in dataSet[key]['heartRate'] if x != 0]
        dataSet[key]['symbol'] = [x for x in dataSet[key]['symbol'] if x != 0]

        newDataSetList = []
        for key in dataSet:
            dataSet[key].update({'timeWindow': key})
            newDataSetList.append(dataSet[key])

        newDataSet = {}
        for counter in range(0, len(newDataSetList)):
            if newDataSetList[counter]['segmentType'] == 0 and counter > 0:
                newCounter = counter
                prevTime = []
                prevSymbol = []
                prevHeartRate = []
                prevMovingTime = []
                prevTotalTime = []
                rightPrevMovingStep = []
                rightPrevMovingTime = 0
                prevNonMovingLength = 0
                prevTimeWindow = ''
                prevLabel = 0

                length = len(newDataSetList[counter]['heartRate'])
                while length >= self.minDuration and newCounter - 1 >= 0:
                    newCounter -= 1
                    test3 = newDataSetList[newCounter]
                    test2 = newDataSetList[newCounter]['timeWindow']
                    print(test2)
                    if '0515_2018_001_000' == test2:
                        print('hi')
                    if newDataSetList[newCounter]['segmentType'] == 0:
                        currHour = newDataSetList[counter]['time'][0][0:newDataSetList[counter]['time'][0].rfind(':')]
                        prevHourValue = newDataSetList[newCounter]['time'][len(newDataSetList[newCounter]['time']) - 1]
                        prevHour = prevHourValue[0:prevHourValue.rfind(':')]
                        currMin = newDataSetList[counter]['time'][0][
                                  newDataSetList[counter]['time'][0].rfind(':') + 1:len(
                                      newDataSetList[counter]['time'][0])]
                        prevMin = prevHourValue[prevHourValue.rfind(':') + 1:len(prevHourValue)]

                        if newDataSetList[counter]['timeWindow'][0:4] != newDataSetList[newCounter]['timeWindow'][0:4]:
                            if len(prevTime) == 0:
                                tempHrReal = hrAvgReal[int(currHour)]['avg']
                                tempHrSymbol = hrAvgSymbol[int(currHour)]['avg']
                                tempTime = '{}{}{}'.format(currHour, ':', '00')

                                tempPrevTime = []
                                tempPrevSymbol = []
                                tempPrevHeartRate = []
                                tempPrevTimeWindow = []

                                for tempCounter in range(0, self.minDuration + 1):
                                    tempPrevTime.append(tempTime)
                                    tempPrevSymbol.append(tempHrSymbol)
                                    tempPrevHeartRate.append(tempHrReal)
                                    tempPrevTimeWindow.append('dummy')

                                prevTime = tempPrevTime
                                prevSymbol = tempPrevSymbol
                                prevHeartRate = tempPrevHeartRate
                                prevTimeWindow = tempPrevTimeWindow
                                prevLabel = 0
                            break

                        if (int(currHour) * 60 + int(currMin)) - (int(prevHour) * 60 + int(prevMin)) > 30:
                            if len(prevTime) == 0:
                                tempHrReal = hrAvgReal[int(currHour)]['avg']
                                tempHrSymbol = hrAvgSymbol[int(currHour)]['avg']
                                tempTime = '{}{}{}'.format(currHour, ':', '00')

                                tempPrevTime = []
                                tempPrevSymbol = []
                                tempPrevHeartRate = []
                                tempPrevTimeWindow = []

                                for tempCounter in range(0, self.minDuration + 1):
                                    tempPrevTime.append(tempTime)
                                    tempPrevSymbol.append(tempHrSymbol)
                                    tempPrevHeartRate.append(tempHrReal)
                                    tempPrevTimeWindow.append('dummy')

                                prevTime = tempPrevTime
                                prevSymbol = tempPrevSymbol
                                prevHeartRate = tempPrevHeartRate
                                prevTimeWindow = tempPrevTimeWindow
                                prevLabel = 0
                            break

                        if len(newDataSetList[newCounter]['heartRate']) >= self.minDuration:
                            if len(newDataSetList[newCounter]['heartRate']) >= self.minDuration:
                                prevTime = newDataSetList[newCounter]['time']
                                prevSymbol = newDataSetList[newCounter]['symbol']
                                prevHeartRate = newDataSetList[newCounter]['heartRate']
                                prevTimeWindow = newDataSetList[newCounter]['timeWindow']
                                prevLabel = newDataSetList[newCounter]['label']

                                if prevNonMovingLength == 0:
                                    prevNonMovingLength = len(newDataSetList[newCounter]['time'])

                            else:
                                tempHrReal = statistics.mean(newDataSetList[newCounter]['heartRate'])
                                tempHrSymbol = statistics.mean(newDataSetList[newCounter]['symbol'])
                                tempTime = newDataSetList[newCounter]['time'][
                                    len(newDataSetList[newCounter]['time']) - 1]
                                for tempCounter in range(len(newDataSetList[newCounter]['time']), self.minDuration + 1):
                                    newDataSetList[newCounter]['heartRate'].append(tempHrReal)
                                    newDataSetList[newCounter]['symbol'].append(tempHrSymbol)
                                    newDataSetList[newCounter]['time'].append(tempTime)

                                prevTime = newDataSetList[newCounter]['time']
                                prevSymbol = newDataSetList[newCounter]['symbol']
                                prevHeartRate = newDataSetList[newCounter]['heartRate']
                                prevTimeWindow = newDataSetList[newCounter]['timeWindow']
                                prevLabel = newDataSetList[newCounter]['label']

                                if prevNonMovingLength == 0:
                                    prevNonMovingLength = len(newDataSetList[newCounter]['time'])

                            break
                        else:
                            if prevNonMovingLength == 0:
                                prevNonMovingLength = len(newDataSetList[newCounter]['time'])
                    else:
                        currHour = newDataSetList[counter]['time'][0][0:newDataSetList[counter]['time'][0].rfind(':')]
                        prevHour = newDataSetList[newCounter]['time'][len(newDataSetList[newCounter]['time']) - 1][
                                   0:newDataSetList[newCounter]['time'][
                                       len(newDataSetList[newCounter]['time']) - 1].rfind(
                                       ':')]

                        prevHour2 = newDataSetList[newCounter]['time'][0][
                                    0:newDataSetList[newCounter]['time'][0].rfind(':')]
                        currMin = newDataSetList[counter]['time'][0][
                                  newDataSetList[counter]['time'][0].rfind(':') + 1:len(
                                      newDataSetList[counter]['time'][0])]
                        prevMin = newDataSetList[newCounter]['time'][0][
                                  newDataSetList[newCounter]['time'][0].rfind(':') + 1:len(
                                      newDataSetList[newCounter]['time'][0])]
                        diff = counter - newCounter
                        length = len(newDataSetList[counter]['heartRate'])

                        movingCounter = newCounter
                        test11 = newDataSetList[counter]['timeWindow']
                        timeDiff = (int(currHour) - int(prevHour2)) * 60 + (int(currMin) - int(prevMin))
                        if len(prevMovingTime) == 0 and timeDiff <= 30 and timeDiff > 0:
                            for value in newDataSetList[newCounter]['time']:
                                prevMovingTime.append(value)
                                prevTotalTime.append(value)

                            for value in newDataSetList[newCounter]['step']:
                                rightPrevMovingStep.append(value)

                            rightPrevMovingTime = int(len(rightPrevMovingStep))

                            while movingCounter - 1 >= 0:
                                movingCounter -= 1
                                if newDataSetList[movingCounter]['segmentType'] == 1:
                                    for i in range(0, len(newDataSetList[movingCounter]['time'])):
                                        value = newDataSetList[movingCounter]['time'][
                                            len(newDataSetList[movingCounter]['time']) - i - 1]
                                        prevMovingHour = int(value[0:value.rfind(':')])
                                        prevMovingMin = int(value[value.rfind(':') + 1:len(value)])
                                        timeDiff = (int(currHour) - prevMovingHour) * 60 + (
                                                int(currMin) - prevMovingMin)
                                        if timeDiff <= 30 and timeDiff > 0:
                                            prevMovingTime.append(value)
                                            prevTotalTime.append(value)
                                        else:
                                            movingCounter = -1
                                            break
                                else:
                                    for i in range(0, len(newDataSetList[movingCounter]['time'])):
                                        value = newDataSetList[movingCounter]['time'][
                                            len(newDataSetList[movingCounter]['time']) - i - 1]
                                        prevMovingHour = int(value[0:value.rfind(':')])
                                        prevMovingMin = int(value[value.rfind(':') + 1:len(value)])
                                        timeDiff = (int(currHour) - prevMovingHour) * 60 + (
                                                int(currMin) - prevMovingMin)
                                        if timeDiff <= 30 and timeDiff > 0:
                                            prevTotalTime.append(value)
                                        else:
                                            break

                        # 집에 오자마자 밥먹는 케이스. NM 세그먼트 이전에 아무것도 없을때만.
                        if int(currHour) - int(prevHour) > 1 and diff == 1 and length >= self.minDuration:
                            # print(newDataSetList[counter]['timeWindow'])
                            tempHrReal = hrAvgReal[int(currHour)]['avg']
                            tempHrSymbol = hrAvgSymbol[int(currHour)]['avg']
                            tempTime = '{}{}{}'.format(currHour, ':', '00')

                            tempPrevTime = []
                            tempPrevSymbol = []
                            tempPrevHeartRate = []
                            tempPrevTimeWindow = []

                            for tempCounter in range(0, self.minDuration + 1):
                                tempPrevTime.append(tempTime)
                                tempPrevSymbol.append(tempHrSymbol)
                                tempPrevHeartRate.append(tempHrReal)
                                tempPrevTimeWindow.append('dummy')

                            prevTime = tempPrevTime
                            prevSymbol = tempPrevSymbol
                            prevHeartRate = tempPrevHeartRate
                            prevTimeWindow = tempPrevTimeWindow
                            prevLabel = 0
                            break

                if len(prevTime) != 0:
                    test100 = newDataSetList[counter]['timeWindow']
                    newDataSetList[counter].update({'prevSegmentType': 0})
                    newDataSetList[counter].update({'prevTime': prevTime})
                    newDataSetList[counter].update({'prevSymbol': prevSymbol})
                    newDataSetList[counter].update({'prevHeartRate': prevHeartRate})
                    newDataSetList[counter].update({'prevTimeWindow': prevTimeWindow})
                    newDataSetList[counter].update({'prevLabel': prevLabel})
                    newDataSetList[counter].update({'prevMovingTime': prevMovingTime})
                    newDataSetList[counter].update({'prevTotalTime': prevTotalTime})
                    newDataSetList[counter].update({'rightPrevMovingStep': rightPrevMovingStep})
                    newDataSetList[counter].update({'rightPrevMovingTime': rightPrevMovingTime})
                    newDataSetList[counter].update({'prevNonMovingLength': prevNonMovingLength})

                    newDataSet.update({newDataSetList[counter]['timeWindow']: newDataSetList[counter]})
                    prevMovingTime = []
                    prevTotalTime = []
                    rightPrevMovingStep = []
                    rightPrevMovingTime = 0
                    prevNonMovingLength = 0

        newResultSet = {}
        for key in newDataSet:
            if len(newDataSet[key]['heartRate']) >= self.minDuration:
                newResultSet.update({key: newDataSet[key]})

        print(len(newDataSet), ',', len(newResultSet))
        return newResultSet

    def _get_peak_heart_rate(self, hr: list) -> list:
        prevMean = 0
        prevHr = []
        for i in range(0, len(hr)):
            if len(hr) - i >= self.minDuration:
                subHr = hr[i:i + self.minDuration]
                if statistics.mean(subHr) > prevMean:
                    prevMean = statistics.mean(subHr)
                    prevHr = subHr
            else:
                break

        return prevHr

    def buildSampleSetWithHRandPrevSeg(self):
        self._buildSampleSetWithHRandPrevSeg('morning')
        self._buildSampleSetWithHRandPrevSeg('evening')
        self._buildSampleSetWithHRandPrevSeg('afternoon')

    def _buildSampleSetWithHRandPrevSeg(self, timeType: str):
        dataSet = self._addPrevPrevSegment(timeType)
        print(len(dataSet))
        dataSet = OrderedDict(sorted(dataSet.items()))

        resultSet = {}
        # prevKey = ''
        for key in dataSet:
            if int(dataSet[key]['label']) == 1:
                self._segmentSize.append(len(dataSet[key]['time']))

            if key == '0524_2018_221_012':
                print(dataSet[key])

            # if key == '0515_2018_102_000':
            #     print('hi')
            if timeType == dataSet[key]['timeType']:
                currHeartRate = dataSet[key]['symbol']
                prevHeartRate = dataSet[key]['prevSymbol']
                # currHeartRate = dataSet[key]['heartRate']
                # prevHeartRate = dataSet[key]['prevHeartRate']
                newCurrHeartRate = []
                newPevHeartRate = []
                for counter in range(0, len(currHeartRate)):
                    if int(currHeartRate[counter]) != 0:
                        newCurrHeartRate.append(currHeartRate[counter])

                for counter in range(0, len(prevHeartRate)):
                    if int(prevHeartRate[counter]) != 0:
                        newPevHeartRate.append(prevHeartRate[counter])

                if len(newCurrHeartRate) >= self.minDuration:
                    subResultSet = {}
                    if len(newPevHeartRate) < self.minDuration:
                        # when the length of prevHeartRate is less than 5, add average hr of that time.
                        # print(newCurrHeartRate)
                        timeBand = int(dataSet[key]['time'][0][0:dataSet[key]['time'][0].rfind(':')])
                        tempHr = statistics.mean(newCurrHeartRate)
                        newPevHeartRate = []
                        for counter in range(len(newPevHeartRate), self.minDuration):
                            newPevHeartRate.append(tempHr)

                    subResultSet.update({'timeWindow': dataSet[key]['timeWindow']})
                    subResultSet.update({'prevTimeWindow': dataSet[key]['prevTimeWindow']})
                    subResultSet.update({'prevLabel': dataSet[key]['prevLabel']})
                    subResultSet.update({'heartRate': newCurrHeartRate})
                    subResultSet.update({'prevHeartRate': newPevHeartRate})
                    subResultSet.update({'time': dataSet[key]['time'][0]})
                    subResultSet.update({'label': dataSet[key]['label']})
                    subResultSet.update({'rightPrevMovingStep': dataSet[key]['rightPrevMovingStep']})
                    subResultSet.update({'rightPrevMovingTime': dataSet[key]['rightPrevMovingTime']})
                    subResultSet.update({'prevMovingTime': len(dataSet[key]['prevMovingTime'])})
                    subResultSet.update({'prevTotalTime': len(dataSet[key]['prevTotalTime'])})
                    subResultSet.update({'prevNonMovingLength': dataSet[key]['prevNonMovingLength']})

                    resultSet.update({dataSet[key]['timeWindow']: subResultSet})

        resultSet = OrderedDict(sorted(resultSet.items()))

        csvWrite = csv.writer(
            open(
                '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/sampleSet_' + timeType + '.csv',
                'w'),
            delimiter=',', quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in resultSet:
            rowList = []
            rowList.append(key)
            if key == '0515_2018_102_000':
                print('hi')
            prevHeartRate = []
            for i in range(0, len(resultSet[key]['prevHeartRate'])):
                prevHeartRate.append(resultSet[key]['prevHeartRate'][i])

            if len(prevHeartRate) > self.minDuration:
                prevHeartRate = self._get_peak_heart_rate(prevHeartRate)

            rowList.append(round(statistics.mean(prevHeartRate), 2))

            currHeartRate = []
            for i in range(0, len(resultSet[key]['heartRate'])):
                currHeartRate.append(resultSet[key]['heartRate'][i])

            currHeartRate = self._get_peak_heart_rate(currHeartRate)

            rowList.append(round(statistics.mean(currHeartRate[0:9]), 2))
            rowList.append(round(float(rowList[2]) - float(rowList[1]), 2))

            rowList.append(resultSet[key]['prevNonMovingLength'])

            rowList.append(resultSet[key]['rightPrevMovingTime'])
            rowList.append(sum(resultSet[key]['rightPrevMovingStep']))

            if resultSet[key]['prevMovingTime'] == 0:
                rowList.append(0)
            else:
                if int(resultSet[key]['prevTotalTime']) >= 30:
                    rowList.append(round((float(resultSet[key]['prevMovingTime']) / 30) * 10, 2))
                else:
                    rowList.append(
                        round((float(resultSet[key]['prevMovingTime']) / float(resultSet[key]['prevTotalTime'])) * 10,
                              2))

            X_10 = currHeartRate[1:self.minDuration]
            X_5 = currHeartRate[1:5]

            value = []
            for i in range(0, len(X_10) - 1):
                value.append(int(X_10[i + 1] - X_10[i]))

            if '0531_2018_212_000' == key:
                print('hi')
            slope_10 = sum(value)

            value = []
            for i in range(0, len(X_5) - 1):
                value.append(int(X_5[i + 1] - X_5[i]))

            slope_5 = sum(value)

            if self._timeType == 'morning':
                rowList.append(max(slope_5, slope_10))
            else:
                rowList.append(slope_10)

            # rowList.append(max(slope_5, slope_10))
            rowList.append(resultSet[key]['label'])
            if rowList[2] > rowList[1] and rowList[7] < 1:
                print('skip')
            else:
                csvWrite.writerow(rowList)

    def mergeJordanSampleData(self):
        self._mergeJordanSampleData('evening')
        self._mergeJordanSampleData('morning')

    def _mergeJordanSampleData(self, timeType: str):
        if 'Jordan' in self._segmentPath:
            total = []

            with open(
                    '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/sampleSet_' + timeType + '.csv') as csvfile:
                readCSV2 = csv.reader(csvfile, delimiter=',')

                for row in readCSV2:
                    subList = []
                    for i in range(0, len(row)):
                        subList.append(row[i])

                    total.append(subList)

            with open('/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/prevSampleSet_Jodan.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')

                for row in readCSV:
                    subList = []
                    for i in range(0, len(row)):
                        subList.append(row[i])

                    total.append(subList)

            csvWrite = csv.writer(
                open(
                    '/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/Merged/sampleSet_' + timeType + '_merged.csv',
                    'w'),
                delimiter=',', quotechar='|',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for i in range(0, len(total)):
                subList = total[i]
                csvWrite.writerow(subList)

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
            dailyActivity = total[key]['dailyActivity']

            dataSet = {}
            heartRateArray = []
            timeArray = []
            stepArray = []
            prevSegmentType = ''
            segCounter = 0

            for counter in range(0, len(heartRate)):
                time = str(hour) + ':' + str(baseMinute)
                baseMinute += 1
                if baseMinute >= 60:
                    baseMinute = 0
                    hour += 1

                if len(heartRate) <= len(step):
                    segmentType = makeDataShared._getSegmentType(makeDataShared, step[counter])

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
                                    heartRate) - 1 and prevSegmentType == 1 and segmentType == 0 and makeDataShared._getSegmentType(
                                makeDataShared,
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

    def isEating(self, date: str, startTimeWindow: int) -> bool:

        segment_data = self._segmentData[date]
        segment = []
        for value in segment_data:
            segment.append(int(value))

        segment.sort()

        threshold = 0

        if self._timeType == 'evening':
            threshold = 205
        elif self._timeType == 'afternoon':
            threshold = 144
        else:
            threshold = 72

        result = False
        for i in range(0, len(segment)):
            if int(segment[i]) >= threshold and int(segment[i]) < startTimeWindow:
                daily_activity = segment_data[str(segment[i])]['dailyActivitySet'][0]['KEY_DAILYACTIVITY']
                if daily_activity == 'eating':
                    result = True
                    return result

        return result

    def _get_labeled_home_event_with_going(self, path: str) -> None:
        data = json.load(open(path))
        total = {}

        for date in data:
            object = data[date]

            for timeWindow in object:
                if '0513' in date:
                    print(timeWindow)

                if '2018' in date and timeWindow != None and isinstance(timeWindow, str):
                    segment = object[timeWindow]
                    if 'heartRate' in segment:
                        dailyActivity = segment['dailyActivitySet'][0]['KEY_DAILYACTIVITY']

                        venueNameArrival = segment['dailyActivitySet'][0]['KEY_S_L_VENUE_NAME_ARRIVAL']
                        venueNameDeparture = segment['dailyActivitySet'][0]['KEY_S_L_VENUE_NAME_DEPARTURE']
                        segmentType = 0
                        if dailyActivity == 'going' and venueNameArrival == 'home' and venueNameDeparture == 'home':
                            dailyActivity = 'home event'
                            segmentType = 1

                        if dailyActivity == 'home event':
                            dataSet = {}
                            if 'heartRate' in segment and 'step' in segment:
                                dataSet.update({'heartRate': segment['heartRate']})
                                dataSet.update({'step': segment['step']})
                                dataSet.update({'activtyLevel': segment['activtyLevel']})
                                dataSet.update({'segmentType': segmentType})
                                dataSet.update({'dailyActivity': dailyActivity})

                                timeWindow = '{0:03d}'.format(int(timeWindow))
                                key = '{}{}{}'.format(date, '_', timeWindow)

                                if 'Pooya' in path:
                                    if date not in self.pooya_skip:
                                        if int(date[0:4]) >= 403:
                                            total[key] = dataSet
                                elif 'Ramesh' in path:
                                    if date not in self.ramesh_skip:
                                        total[key] = dataSet
                                elif 'Jordan' in path:
                                    if date not in self.jordan_skip:
                                        total[key] = dataSet
                                else:
                                    total[key] = dataSet

        return total

    def convertContinuousToDiscrete(self) -> None:
        # if 'Jordan' in self._segmentPath:

        total = self._get_labeled_home_event_with_going(self._segmentPath)
        if self._name == 'Ramesh':
            newSegmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-Ramesh-0515-2018.json'
            newTotal = self._get_labeled_home_event_with_going(newSegmentPath)
            for value in total:
                newTotal.update({value: total[value]})

            total = newTotal

        segmentTotal = self._segment(total)

        heartRateMorningWhileNonMoving = []
        keyMorningWhileNonMoving = []
        heartRateMorningWhileMoving = []
        keyMorningWhileMoving = []
        heartRateAfternoonWhileNonMoving = []
        keyAfternoonWhileNonMoving = []
        heartRateAfternoonWhileMoving = []
        keyAfternoonWhileMoving = []
        heartRateEveningWhileNonMoving = []
        keyEveningWhileNonMoving = []
        heartRateEveningWhileMoving = []
        keyEveningWhileMoving = []

        mCount = 0
        mDelta = 0
        mAvg = 0
        mM2 = 0
        mStv = 0

        for key in segmentTotal:
            timeList = segmentTotal[key]['time']
            heartRateList = segmentTotal[key]['heartRate']
            segmentType = segmentTotal[key]['segmentType']

            if segmentType == 0:
                for counter in range(0, len(timeList)):
                    timeBand = int(timeList[counter][0:timeList[counter].rfind(':')])
                    heartRateValue = int(heartRateList[counter])
                    if heartRateValue != 0:
                        if timeBand >= 17 and timeBand < 24:
                            heartRateEveningWhileNonMoving.append(heartRateValue)
                            keyEveningWhileNonMoving.append(key)
                        elif timeBand > 11 and timeBand < 17:
                            heartRateAfternoonWhileNonMoving.append(heartRateValue)
                            keyAfternoonWhileNonMoving.append(key)
                        else:
                            mCount = mCount + 1
                            mDelta = heartRateValue - mAvg
                            mAvg = mAvg + mDelta / mCount
                            mM2 = mM2 + mDelta * (heartRateValue - mAvg)
                            mStv = math.sqrt(mM2 / mCount)
                            heartRateMorningWhileNonMoving.append(heartRateValue)
                            keyMorningWhileNonMoving.append(key)
            else:
                for counter in range(0, len(timeList)):
                    timeBand = int(timeList[counter][0:timeList[counter].rfind(':')])
                    heartRateValue = int(heartRateList[counter])
                    if heartRateValue != 0:
                        if timeBand >= 17 and timeBand < 24:
                            heartRateEveningWhileMoving.append(heartRateValue)
                            keyEveningWhileMoving.append(key)
                        elif timeBand > 11 and timeBand < 17:
                            heartRateAfternoonWhileMoving.append(heartRateValue)
                            keyAfternoonWhileMoving.append(key)
                        else:
                            heartRateMorningWhileMoving.append(heartRateValue)
                            keyMorningWhileMoving.append(key)

        sd_morning_nonMoving = np.std(np.array(heartRateMorningWhileNonMoving))
        mean_morning_nonMoving = np.mean(np.array(heartRateMorningWhileNonMoving))

        # plt.hist(heartRateMorningWhileMoving, bins=10)
        # plt.ylabel('No of times')
        # plt.show()

        sd_afternoon_nonMoving = np.std(np.array(heartRateAfternoonWhileNonMoving))
        mean_afternoon_nonMoving = np.mean(np.array(heartRateAfternoonWhileNonMoving))

        sd_evening_nonMoving = np.std(np.array(heartRateEveningWhileNonMoving))
        mean_evening_nonMoving = np.mean(np.array(heartRateEveningWhileNonMoving))

        sd_morning_moving = np.std(np.array(heartRateMorningWhileMoving))
        mean_morning_moving = np.mean(np.array(heartRateMorningWhileMoving))

        sd_afternoon_moving = np.std(np.array(heartRateAfternoonWhileMoving))
        mean_afternoon_moving = np.mean(np.array(heartRateAfternoonWhileMoving))

        sd_evening_moving = np.std(np.array(heartRateEveningWhileMoving))
        mean_evening_moving = np.mean(np.array(heartRateEveningWhileMoving))

        for key in segmentTotal:
            timeList = segmentTotal[key]['time']
            heartRateList = segmentTotal[key]['heartRate']
            segmentType = segmentTotal[key]['segmentType']
            symbolic = []
            # symbolicTest = []
            newCount = 0

            if segmentType == 1:
                for counter in range(0, len(timeList)):
                    timeBand = int(timeList[counter][0:timeList[counter].rfind(':')])
                    heartRateValue = int(heartRateList[counter])

                    if 17 <= timeBand < 24:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(
                                self._continous_to_symbolic2(heartRateValue, sd_evening_moving, mean_evening_moving))
                            # series = (heartRateValue - mean_evening_moving) / sd_evening_moving
                            # symbolicTest.append(self._test_convert(series))
                    elif 11 < timeBand < 17:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(self._continous_to_symbolic2(heartRateValue, sd_afternoon_moving,
                                                                         mean_afternoon_moving))
                            # series = (heartRateValue - mean_afternoon_moving) / sd_afternoon_moving
                            # symbolicTest.append(self._test_convert(series))

                    else:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(
                                self._continous_to_symbolic2(heartRateValue, sd_morning_moving, mean_morning_moving))
                            # series = (heartRateValue - mean_morning_moving) / sd_morning_moving
                            # symbolicTest.append(self._test_convert(series))

            else:
                for counter in range(0, len(timeList)):
                    timeBand = int(timeList[counter][0:timeList[counter].rfind(':')])
                    heartRateValue = int(heartRateList[counter])

                    if timeBand >= 17 and timeBand < 24:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(self._continous_to_symbolic2(heartRateValue, sd_evening_nonMoving,
                                                                         mean_evening_nonMoving))
                            # series = (heartRateValue - mean_evening_nonMoving) / sd_evening_nonMoving
                            # symbolicTest.append(self._test_convert(series))

                    elif timeBand > 11 and timeBand < 17:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(self._continous_to_symbolic2(heartRateValue, sd_afternoon_nonMoving,
                                                                         mean_afternoon_nonMoving))
                            # series = (heartRateValue - mean_afternoon_nonMoving) / sd_afternoon_nonMoving
                            # symbolicTest.append(self._test_convert(series))

                    else:
                        if heartRateValue == 0:
                            symbolic.append(0)
                        else:
                            symbolic.append(self._continous_to_symbolic2(heartRateValue, sd_morning_nonMoving,
                                                                         mean_morning_nonMoving))
                            # series = (heartRateValue - mean_morning_nonMoving) / sd_morning_nonMoving
                            # symbolicTest.append(self._test_convert(series))

            segmentTotal[key].update({'symbolic': symbolic})

        csvWrite = csv.writer(
            open('/Users/hyungiko/Desktop/Personicle Data/' + self._name + '/symbolicResultHomeEvent.csv', 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for key in segmentTotal:
            time = segmentTotal[key]['time']
            heartRate = segmentTotal[key]['heartRate']
            step = segmentTotal[key]['step']
            symbol = segmentTotal[key]['symbolic']
            segmentType = segmentTotal[key]['segmentType']
            dailyActivity = segmentTotal[key]['dailyActivity']

            for counter in range(0, len(heartRate)):
                csvWrite.writerow([key, time[counter], heartRate[counter], step[counter], symbol[counter],
                                   segmentType, dailyActivity])

    def _test_convert(self, series) -> int:
        if series < -1.2815515655446:
            return 1
        elif -1.2815515655446 <= series < -0.841621233572914:
            return 2
        elif -0.841621233572914 <= series < -0.524400512708041:
            return 3
        elif -0.524400512708041 <= series < -0.2533471031358:
            return 4
        elif -0.2533471031358 <= series < 0:
            return 5
        elif 0 <= series < 0.2533471031358:
            return 6
        elif 0.2533471031358 <= series < 0.524400512708041:
            return 7
        elif 0.524400512708041 <= series < 0.841621233572914:
            return 8
        elif 0.841621233572914 <= series < 1.2815515655446:
            return 9
        else:
            return 10

    def _continous_to_symbolic2(self, hr: int, sd, mean) -> int:
        targetList = [hr]
        dat_target = np.array(targetList)

        dat_znorm = znorm.znorm2(dat_target, sd, mean)
        dat_paa = paa.paa(dat_znorm, len(dat_target))
        symbolicResult = sax.ts_to_string(dat_paa, alphabet.cuts_for_asize(10))

        if symbolicResult[0] == 'a':
            value = 1
        elif symbolicResult[0] == 'b':
            value = 2
        elif symbolicResult[0] == 'c':
            value = 3
        elif symbolicResult[0] == 'd':
            value = 4
        elif symbolicResult[0] == 'e':
            value = 5
        elif symbolicResult[0] == 'f':
            value = 6
        elif symbolicResult[0] == 'g':
            value = 7
        elif symbolicResult[0] == 'h':
            value = 8
        elif symbolicResult[0] == 'i':
            value = 9
        elif symbolicResult[0] == 'j':
            value = 10

        return value

    def _continous_to_symbolic(self, dataList: list, timeList: list) -> dict:

        dat = np.array(dataList)

        dat_znorm = znorm.znorm(dat)
        dat_paa = paa.paa(dat_znorm, len(dataList))
        symbolicResult = sax.ts_to_string(dat_paa, alphabet.cuts_for_asize(10))

        newDataSet = {}
        for i in range(0, len(symbolicResult)):
            value = 0
            if symbolicResult[i] == 'a':
                value = 1
            elif symbolicResult[i] == 'b':
                value = 2
            elif symbolicResult[i] == 'c':
                value = 3
            elif symbolicResult[i] == 'd':
                value = 4
            elif symbolicResult[i] == 'e':
                value = 5
            elif symbolicResult[i] == 'f':
                value = 6
            elif symbolicResult[i] == 'g':
                value = 7
            elif symbolicResult[i] == 'h':
                value = 8
            elif symbolicResult[i] == 'i':
                value = 9
            elif symbolicResult[i] == 'j':
                value = 10

            if timeList[i] in newDataSet:
                test = newDataSet[timeList[i]]
                test.append(int(value))
                newDataSet.update({timeList[i]: test})
            else:
                newDataSet.update({timeList[i]: [int(value)]})
        return newDataSet

    def _getSymbolicValue(self, value: int, numbOfSymbol: int, sd, mean) -> int:
        targetList = [value]
        dat_target = np.array(targetList)

        dat_znorm = znorm.znorm2(dat_target, sd, mean)
        dat_paa = paa.paa(dat_znorm, len(dat_target))
        symbolicResult = sax.ts_to_string(dat_paa, alphabet.cuts_for_asize(numbOfSymbol))

        if symbolicResult[0] == 'a':
            value = 0
        elif symbolicResult[0] == 'b':
            value = 1
        elif symbolicResult[0] == 'c':
            value = 2
        elif symbolicResult[0] == 'd':
            value = 3
        elif symbolicResult[0] == 'e':
            value = 4
        elif symbolicResult[0] == 'f':
            value = 5
        elif symbolicResult[0] == 'g':
            value = 6
        elif symbolicResult[0] == 'h':
            value = 7
        elif symbolicResult[0] == 'i':
            value = 8
        elif symbolicResult[0] == 'j':
            value = 9

        return value
