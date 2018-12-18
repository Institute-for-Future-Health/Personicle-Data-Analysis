from collections import OrderedDict

# import alphabet
# import paa
# import sax
# import znorm
import numpy as np

class makeDataShared:
    def getSegmentType(step: int):
        if step > 5:
            return 1
        else:
            return 0

    def _getFilteredSegment(self, segment: dict):
        prevSegmentType = ''
        prevKey = ''
        prevMinute = ''
        prevHour = ''

        newSegment = {}
        for key in segment:

            currMinute = segment[key]['time'][0][
                         segment[key]['time'][0].rfind(':') + 1:len(segment[key]['time'][0])]
            currHour = segment[key]['time'][0][0:segment[key]['time'][0].rfind(':')]

            if prevKey != '':
                if key[0:4] == prevKey[0:4]:
                    if currHour == prevHour and int(currMinute) - int(prevMinute) <= 10 and int(currMinute) - int(
                            prevMinute) > 0:
                        if prevSegmentType == segment[key]['segmentType']:
                            if prevKey in newSegment:
                                newPrevKey = newSegment[prevKey]
                            mergedSegment = makeDataShared._getMergedObject(makeDataShared, newPrevKey, segment[key])
                            newSegment.update({key: mergedSegment})
                            if prevKey in newSegment:
                                newSegment.pop(prevKey)
                        else:
                            newSegment.update({key: segment[key]})
                    elif currHour != prevHour and int(currHour) - int(prevHour) == 1 and int(currMinute) - int(
                            prevMinute) < -55:
                        if prevSegmentType == segment[key]['segmentType']:
                            if prevKey in newSegment:
                                newPrevKey = newSegment[prevKey]
                            mergedSegment = makeDataShared._getMergedObject(makeDataShared, newPrevKey, segment[key])
                            newSegment.update({key: mergedSegment})
                            if prevKey in newSegment:
                                newSegment.pop(prevKey)
                        else:
                            newSegment.update({key: segment[key]})
                    else:
                        newSegment.update({key: segment[key]})
                else:
                    newSegment.update({key: segment[key]})
            else:
                newSegment.update({key: segment[key]})
            prevSegmentType = segment[key]['segmentType']
            prevKey = key
            prevMinute = segment[key]['time'][len(segment[key]['time']) - 1][
                         segment[key]['time'][len(segment[key]['time']) - 1].rfind(':') + 1:len(
                             segment[key]['time'][len(segment[key]['time']) - 1])]

            prevHour = segment[key]['time'][len(segment[key]['time']) - 1][
                       0:segment[key]['time'][len(segment[key]['time']) - 1].rfind(':')]

        newSegment = OrderedDict(sorted(newSegment.items()))
        return newSegment

    def _getMergedObject(self, prev: dict, curr: dict):
        prevTime = prev['time']
        curTime = curr['time']
        prevStep = prev['step']
        curStep = curr['step']
        prevHeartRate = prev['heartRate']
        curHeartRate = curr['heartRate']

        for counter in range(0, len(curTime)):
            prevTime.append(curTime[counter])

        for counter in range(0, len(curStep)):
            prevStep.append(int(curStep[counter]))

        for counter in range(0, len(curHeartRate)):
            prevHeartRate.append(int(curHeartRate[counter]))

        prev.update({'time': prevTime})
        prev.update({'step': prevStep})
        prev.update({'heartRate': prevHeartRate})

        return prev

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

    def convert_symbolic(series) -> int:
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