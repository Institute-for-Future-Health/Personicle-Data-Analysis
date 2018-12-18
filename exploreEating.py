import csv
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats


class explore_eating:

    def __init__(self, data_path: str):
        self._data_path = data_path

    def _get_segment_type(self, step: int):
        if step > 5:
            return 1
        else:
            return 0

    def _get_variation(self, heart_rate: list) -> int:
        variation = 0
        prev_hr = heart_rate[0]
        for value in heart_rate:
            current_hr = value
            temp = current_hr - prev_hr
            variation = variation + temp
            prev_hr = value

        return variation

    def _dual_segment_and_highest_hr(self, key: str, time_stamp: list, heart_rate: list, step: list) -> float:
        prev_seg_type = self._get_segment_type(step[0])

        key_total = []
        heart_rate_total = []
        heart_rate_temp = []
        step_total = []
        step_temp = []
        time_stamp_total = []
        time_stamp_temp = []
        count_temp = 0

        for count in range(0, len(step)):
            if prev_seg_type == self._get_segment_type(step[count]):
                heart_rate_temp.append(heart_rate[count])
                step_temp.append(step[count])
                time_stamp_temp.append(time_stamp[count])
            else:
                if prev_seg_type == 0:
                    key_total.append('{}{}{}'.format(key, '_', count_temp))
                    heart_rate_total.append(heart_rate_temp)
                    step_total.append(step_temp)
                    time_stamp_total.append(time_stamp_temp)
                heart_rate_temp = [heart_rate[count]]
                step_temp = [step[count]]
                time_stamp_temp = [time_stamp[count]]
                count_temp = count_temp + 1

            if count == len(step) - 1 and prev_seg_type == 0:
                key_total.append('{}{}{}'.format(key, '_', count_temp))
                heart_rate_total.append(heart_rate_temp)
                step_total.append(step_temp)
                time_stamp_total.append(time_stamp_temp)

            prev_seg_type = self._get_segment_type(step[count])

        highest_hr = []
        prev_hr = []

        time_window_size = 8

        for heart_rate_temp in heart_rate_total:
            length = len(heart_rate_temp)
            for count in range(0, length):
                if count + time_window_size <= length:
                    if len(prev_hr) != 0:
                        current_hr = heart_rate_temp[count:count + time_window_size]
                        print(current_hr, ' ,', np.sum(np.array(current_hr)) - np.sum(np.array(prev_hr)), ',',
                              self._get_variation(current_hr), ',', prev_hr)

                    prev_hr = np.array(heart_rate_temp[count:count + time_window_size])

                    if np.sum(np.array(highest_hr)) < np.sum(np.array(heart_rate_temp[count:count + time_window_size])):
                        highest_hr = heart_rate_temp[count:count + time_window_size]
                else:
                    break
        # find the highest hr pattern

        # print(highest_hr, ',' ,)
        return highest_hr

    def test(self):
        with open(self._data_path) as csvfile:
            # isFull = False
            count = 0
            prev_date = ''
            readCSV = csv.reader(csvfile, delimiter=',')
            hr = []
            hr_1 = []
            hr_2 = []
            hr_4 = []
            hr_8 = []
            for row in readCSV:
                cur_date = row[0][0:9]
                step = int(row[3])
                time = row[1]

                timeBand = int(time[0:time.rfind(':')])
                # if 6 <= timeBand <= 11:
                if 17 <= timeBand < 24:
                    if step <= 4 and int(row[2]) != 0:
                        hr.append(int(row[2]))

                    if prev_date != '' and prev_date == cur_date and count == 0:
                        if step <= 4 and int(row[2]) != 0:
                            hr_1.append(int(row[2]))

                    if prev_date != '' and prev_date == cur_date and 0 <= count <= 1:
                        if step <= 4 and int(row[2]) != 0:
                            hr_2.append(int(row[2]))

                    if prev_date != '' and prev_date == cur_date and 0 <= count <= 2:
                        if step <= 4 and int(row[2]) != 0:
                            hr_4.append(int(row[2]))

                    if prev_date != '' and prev_date == cur_date and 0 <= count <= 7:
                        if step <= 4 and int(row[2]) != 0:
                            hr_8.append(int(row[2]))

                if prev_date != '' and prev_date != cur_date:
                    count = count + 1

                prev_date = cur_date
        #
        ax1 = plt.subplot(221)
        res = stats.probplot(hr_1, plot=plt)
        plt.title('Probability Plot - 1st day')
        plt.xlabel('')
        ax2 = plt.subplot(222)
        res = stats.probplot(hr_2, plot=plt)
        plt.title('Probability Plot - 2nd day')
        plt.xlabel('')

        ax2 = plt.subplot(223)
        res = stats.probplot(hr_4, plot=plt)
        plt.title('Probability Plot - 4th day')
        # plt.xlabel('')

        ax2 = plt.subplot(224)
        res = stats.probplot(hr, plot=plt)
        plt.title('Probability Plot - 8th day')
        # plt.xlabel('')

        mean_1 = np.mean(np.array(hr_1))
        std_1 = np.std(np.array(hr_1))
        print(self._getSymbolicValue(70, 10, std_1, mean_1))

        mean_2 = np.mean(np.array(hr_2))
        std_2 = np.std(np.array(hr_2))
        print(self._getSymbolicValue(70, 10, std_2, mean_2))

        mean_4 = np.mean(np.array(hr_4))
        std_4 = np.std(np.array(hr_4))
        print(self._getSymbolicValue(70, 10, std_4, mean_4))

        mean = np.mean(np.array(hr))
        std = np.std(np.array(hr))
        print(self._getSymbolicValue(70, 10, std, mean))

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

    def get_sample_set(self) -> dict:
        with open(self._data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            sub_segment = {}
            time_stamp = []
            heart_rate = []
            step = []

            prev_date = ''
            prev_venue = ''
            for row in readCSV:
                if prev_date == '':
                    prev_date = row[0]
                    prev_venue = row[5]

                if prev_date == row[0]:
                    time_stamp.append(row[1])
                    heart_rate.append(int(row[2]))
                    step.append(int(row[3]))
                else:
                    highest_hr_avg = self._dual_segment_and_highest_hr(prev_date, time_stamp, heart_rate, step)
                    if len(highest_hr_avg) != 0:
                        sub_segment_temp = {}
                        sub_segment_temp.update({'highest_hr': highest_hr_avg})
                        sub_segment_temp.update({'venue_name': prev_venue})
                        sub_segment.update({prev_date: sub_segment_temp})
                        print(prev_date, ',', np.mean(np.array(highest_hr_avg)), ',', prev_venue)
                    time_stamp = [row[1]]
                    heart_rate = [int(row[2])]
                    step = [int(row[3])]

                prev_date = row[0]
                prev_venue = row[5]

            return sub_segment

    def draw_the_highest_hr_plot(self, sample_set: dict):
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        for key in sample_set:
            print(sample_set[key])
            plt.plot(x, sample_set[key]['highest_hr'])
