import csv
import operator
from pathlib import Path

import numpy as np
import math
import scipy.signal
import matplotlib.pyplot as plt
from numpy.core.umath import degrees
from scipy.stats import linregress


class structuralFeature:
    def __init__(self):
        self._type = 'breakfast'
        self._is_home = True
        # self._is_home = False

        self._uniq_time_windpw = set()
        self._get_data()
        self._key = '1206_2018_084_004'

        if self._is_home:
            if self._type == 'dinner':
                self._file_name = 'dinner_home_data'
            elif self._type == 'lunch':
                self._file_name = 'lunch_home_data'
            elif self._type == 'breakfast':
                self._file_name = 'breakfast_home_data'
        else:
            self._file_name = 'restaurant_data'

        #################################
        # Drawing whole plots
        self._draw_plot()

        #################################
        # Update features - cc, peak
        # self._update_feature()

        #################################
        # Finding features from a plot

        self._default_var()

        # self._begin = 5
        # self._up_start = 5
        # self._max = 12
        # self._down_start = 12
        # self._end = 20
        # self._peak_set = [12]

        self._get_feature()

        #################################

        # self._get_smoothed_hr('0925_2018_215_005')
        # for time_window in self._uniq_time_windpw:
        #     self._get_smoothed_hr(time_window)

    def _draw_plot(self):
        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/' + self._file_name + '.csv'

        with open(data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                key = row[0]
                if key == '0808_2018_157_000':
                    print('hi')
                if key != 'key':
                    original_hr = self._data[key]['heart_rate']
                    smoothing_hr = scipy.signal.medfilt(original_hr)
                    # smoothing_hr = original_hr
                    x = np.arange(0., len(original_hr), 1)

                    begin = int(row[17])
                    up_start = int(row[18])
                    max = int(row[19])
                    down_start = int(row[20])
                    end = int(row[21])

                    plt.axvline(x=begin, color='m')
                    plt.axvline(x=up_start, color='r')
                    plt.axvline(x=max, color='y')
                    plt.axvline(x=down_start, color='c')
                    plt.axvline(x=end, color='b')

                    plt.title(key+':'+row[len(row)-1])
                    plt.plot(x, smoothing_hr)
                    plt.show()

    def _update_feature(self):
        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/' + self._file_name + '.csv'

        with open(data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                key = row[0]
                # if key == '0808_2018_157_000':
                #     print('hi')
                if key != 'key':
                    if row[13] == '':
                        original_hr = self._data[key]['heart_rate']
                        smoothing_hr = scipy.signal.medfilt(original_hr)
                        # smoothing_hr = original_hr
                        x = np.arange(0., len(original_hr), 1)

                        begin = int(row[17])
                        up_start = int(row[18])
                        max = int(row[19])
                        down_start = int(row[20])
                        end = int(row[21])

                        plt.axvline(x=begin, color='m')
                        plt.axvline(x=up_start, color='r')
                        plt.axvline(x=max, color='y')
                        plt.axvline(x=down_start, color='c')
                        plt.axvline(x=end, color='b')

                        plt.title(key)
                        plt.plot(x, smoothing_hr)
                        plt.show()

                        self._default_var()
                        x = input('Enter peaks:')
                        if ',' in x:
                            x = x.split(',')
                            x = list(map(int, x))
                            self._peak_set = x
                        else:
                            self._peak_set.append(int(x))

                        self._key = row[0]
                        self._begin = begin
                        self._up_start = up_start
                        self._max = max
                        self._down_start = down_start
                        self._end = end

                        self._get_feature()

    def _default_var(self):
        self._begin = 0
        self._start = 0
        self._max = 0
        self._end = 0
        self._peak_set = []

    def _get_data(self):
        attribute = ['time_window', 'time_stamp', 'heart_rate', 'step', 'label', 'meal_type', 'symbolic_heart_rate']

        if self._is_home:
            if self._type == 'dinner':
                path = '/Users/hyungiko/Desktop/Personicle Data/eating/split/dinner_home.csv'
            elif self._type == 'lunch':
                path = '/Users/hyungiko/Desktop/Personicle Data/eating/split/lunch_home.csv'
            elif self._type == 'breakfast':
                path = '/Users/hyungiko/Desktop/Personicle Data/eating/split/breakfast_home.csv'
        else:
            path = '/Users/hyungiko/Desktop/Personicle Data/eating/split/jordan2_restaurant.csv'

        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            data_set = {}
            for row in readCSV:
                time_window = row[0]
                self._uniq_time_windpw.add(time_window)
                if time_window not in data_set:
                    temp = {}
                    for count in range(1, len(row)):
                        if attribute[count] == 'label' or attribute[count] == 'meal_type':
                            temp.update({attribute[count]: row[count]})
                        elif attribute[count] == 'heart_rate' or attribute[count] == 'step':
                            temp.update({attribute[count]: [int(row[count])]})
                        else:
                            temp.update({attribute[count]: [row[count]]})

                    data_set.update({time_window: temp})

                else:
                    temp = data_set[time_window]

                    for count in range(1, len(row)):
                        if attribute[count] != 'label' and attribute[count] != 'meal_type':
                            temp_list = temp[attribute[count]]
                            if attribute[count] == 'heart_rate' or attribute[count] == 'step':
                                temp_list.append(int(row[count]))
                            else:
                                temp_list.append(row[count])

                            temp.update({attribute[count]: temp_list})

            self._data = data_set

    def _get_filtered_seq(self, hr: list) -> list:
        slope_list = []

        for count in range(0, len(hr) - 1):
            sample = [hr[count], hr[count + 1]]
            slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)
            slope_list.append(slope)

        prev_slope = -100
        for count in range(0, len(slope_list)):
            if prev_slope != -100 and prev_slope >= 0 and (slope_list[count] == -1 or slope_list[count] == -2) and \
                    slope_list[count + 1] >= 0:
                slope_list[count] = 0

            prev_slope = slope_list[count]

        return slope_list

    def _get_peak(self, hr: list, key: str) -> int:
        # slope_list = self._get_filtered_seq(hr)
        slope_list = []
        for count in range(0, len(hr) - 1):
            sample = [hr[count], hr[count + 1]]
            slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)
            slope_list.append(slope)

        pick_dict = {}
        hr_peak = {}
        count_temp = []
        hr_temp = []

        for count in range(0, len(slope_list)):
            if slope_list[count] >= 0:
                hr_temp.append(hr[count])
                count_temp.append(count)
            else:
                if len(count_temp) != 0:
                    for value in reversed(count_temp):
                        if slope_list[value] != 0:
                            hr_temp.append(hr[count])
                            count_temp.append(count)
                            hr_temp.sort(reverse=True)
                            hr_peak.update({len(pick_dict): hr_temp[0]})
                            pick_dict.update({len(pick_dict): count_temp})
                            break

                count_temp = []
                hr_temp = []

        if len(count_temp) != 0:
            hr_temp.append(hr[count + 1])
            count_temp.append(count + 1)
            hr_temp.sort(reverse=True)
            hr_peak.update({len(pick_dict): hr_temp[0]})
            pick_dict.update({len(pick_dict): count_temp})

        prev_hr = set()
        pop_key = []
        for value in hr_peak:
            print(hr_peak[value])
            if hr_peak[value] in prev_hr:
                pop_key.append(value)

            prev_hr.add(hr_peak[value])

        slope_dict = {}
        print(key)
        for value in pick_dict:
            array_temp = []
            sample_x = []
            count = 0
            is_start = False
            for value2 in pick_dict[value]:
                if value2 < len(pick_dict[value]):
                    if slope_list[value2] != 0:
                        is_start = True

                    if is_start:
                        array_temp.append(hr[value2])
                        sample_x.append(count)
                        count = count + 1

            if len(pick_dict[value]) > 1 and len(sample_x) != 0:
                slope, intercept, r_value, p_value, std_err = linregress(sample_x, array_temp)
                if slope < 0.5 and value not in pop_key:
                    pop_key.append(value)

        for value in pop_key:
            hr_peak.pop(value)

        sorted_x = sorted(hr_peak.items(), key=operator.itemgetter(1))
        peak = 0
        index = 0
        for value in reversed(sorted_x):
            temp = list(pick_dict[value[0]])
            print(temp, ',len: ', len(temp))

            if len(pick_dict[value[0]]) > 2:
                for count in range(len(temp) - 1, -1, -1):
                    test1 = temp[count]
                    test2 = slope_list[temp[count]]
                    # if
                    if slope_list[temp[count]] != 0:
                        peak = value[1]
                        index = temp[count] + 1
                        break
                break

        print(pick_dict)
        return index - 1

    def _get_peak_manual(self, max: int, hr: list) -> int:
        return hr[max]

    def _get_slope(self, start: int, end: int, hr: list) -> dict:
        x = []
        y = []
        result = {}
        for count in range(start, end + 1):
            x.append(count - start)
            y.append(hr[count])

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        height = abs((hr[end] - hr[start]))
        width = len(x) - 1
        tan_theta = degrees(math.atan(height / width))
        result.update({'slope': slope})
        result.update({'height': height})
        result.update({'width': width})
        result.update({'tan': tan_theta})

        return result

    def _get_variation(self, begin: int, max: int, hr: list) -> int:
        return hr[max] - hr[begin]

    def _get_stat(self, start: int, end: int, hr: list) -> dict:
        temp_list = []
        for count in range(start, end + 1):
            temp_list.append(hr[count])

        result = {}
        result.update({'mean': np.mean(np.array(temp_list))})
        result.update({'std': np.std(np.array(temp_list))})

        return result

    def _get_interval_var(self, hr: list) -> dict:
        result = {}
        peak_list = []
        cc_intervar = []
        interval_set = [self._begin]

        count = 0
        prev_index = 0

        for index in self._peak_set:
            interval_set.append(index)
            peak_list.append(hr[index])

        for index in interval_set:
            if count != 0:
                cc_intervar.append(index - prev_index)

            prev_index = index
            count += 1

        if len(cc_intervar) == 0:
            result.update({'cc_avg': 0})
            result.update({'cc_std': 0})
        else:
            result.update({'cc_avg': np.mean(np.array(cc_intervar))})
            result.update({'cc_std': np.std(np.array(cc_intervar))})

        result.update({'peak_avg': np.mean(np.array(peak_list))})
        result.update({'peak_std': np.std(np.array(peak_list))})

        return result

    def _get_feature(self):
        original_hr = self._data[self._key]['heart_rate']
        # original_hr = original_hr[1: len(original_hr)]
        smoothing_hr = scipy.signal.medfilt(original_hr)
        # smoothing_hr = original_hr
        x = np.arange(0., len(original_hr), 1)

        if self._max != 0:
            self._peak = self._get_peak_manual(self._max, smoothing_hr)
            self._increasing_feature = self._get_slope(self._up_start, self._max, smoothing_hr)
            self._variation = self._get_variation(self._begin, self._max, smoothing_hr)
            self._decreasing_feature = self._get_slope(self._down_start, self._end, smoothing_hr)
            self._stat = self._get_stat(self._up_start, self._end, smoothing_hr)
            self._interval_var = self._get_interval_var(smoothing_hr)

            plt.axvline(x=self._begin, color='m')
            plt.axvline(x=self._up_start, color='r')
            plt.axvline(x=self._max, color='y')
            plt.axvline(x=self._down_start, color='c')
            plt.axvline(x=self._end, color='b')

            for var in self._peak_set:
                plt.axvline(x=var, color='y')

            path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/' + self._file_name + '.csv'
            my_file = Path(path)
            if my_file.is_file():
                print('exist')
                self._update_csv(path)
            else:
                self._generate_csv(path)
                print('no')

        plt.title(self._key)
        plt.plot(x, smoothing_hr)
        plt.show()

    def _get_smoothed_hr(self, key: str):
        # key = '0412_2018_227_003'
        original_hr = self._data[key]['heart_rate']
        original_hr = original_hr[1: len(original_hr)]
        smoothing_hr = scipy.signal.medfilt(original_hr)
        x = np.arange(0., len(original_hr), 1)
        # print(original_hr)
        print(smoothing_hr)

        # hr = original_hr
        hr = smoothing_hr

        min_t = -1
        max_t = -1
        end_t = -1

        min_hr = 200
        max_hr = -1
        end_hr = 200

        min_count = 0;

        init = -1
        is_init = False
        is_increasing_pattern = False
        init_hr = -1

        for count in range(0, len(hr)):
            if count < len(hr) - 1:
                sample = [hr[count], hr[count + 1]]
                slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)
                print('count: ', count, ', slope: ', slope)
                # if slope > 0:

                if init == -1 and slope > 0:
                    init = count
                    init_hr = hr[count]
                elif init != -1 and slope < -2 and is_init == False and hr[count] - init_hr <= 5:
                    init = -1
                    is_init = True

            if hr[count] > max_hr:
                max_hr = hr[count]
                max_t = count

        if is_init:
            max_hr = -1
            for count in range(init, len(hr)):
                if hr[count] > max_hr:
                    max_hr = hr[count]
                    max_t = count

        if max_t <= 1:  # try to find a stable hr
            new_count = 0
            for count in range(0, len(hr)):
                sample = [hr[count], hr[count + 1]]
                slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)

                if slope > 0:
                    new_count = count
                    break

            max_hr = -1
            max_t = -1
            for count in range(new_count, len(hr)):
                if hr[count] > max_hr:
                    max_hr = hr[count]
                    max_t = count

        for count in range(min_count, max_t + 1):
            min_count = min_count + 1

            sample = [hr[count], hr[count + 1]]
            slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)

            if slope < 0:
                min_count = min_count - 1

            if hr[count] <= min_hr:
                min_hr = hr[count]
                min_t = count

            if min_count >= 4 and min_hr != 200:
                break

        slope_count = 0
        end_hr = 0
        end_t = 0

        max_slope = -100
        increasing_count = 0
        increasing_count_temp = 0
        max_slope_start_at_temp = 0
        max_slope_start_at = 0
        hr_temp = 0
        hr_real = 200

        for count in range(0, max_t):
            sample = [hr[count], hr[count + 1]]
            slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)

            if increasing_count_temp == 0 and slope > 0:
                max_slope_start_at_temp = count
                hr_temp = hr[count]

            if slope > 0:
                increasing_count_temp = increasing_count_temp + 1
            elif slope < 0:
                if increasing_count < increasing_count_temp:
                    # if increasing_count < increasing_count_temp and hr_real >= hr_temp:
                    increasing_count = increasing_count_temp
                    max_slope_start_at = max_slope_start_at_temp
                    hr_real = hr_temp

                increasing_count_temp = 0

        if increasing_count < increasing_count_temp:
            # if increasing_count < increasing_count_temp and hr_real >= hr_temp:
            increasing_count = increasing_count_temp
            max_slope_start_at = max_slope_start_at_temp
            hr_real = hr_temp

        print('max_slope_start_at: ', max_slope_start_at, ', increasing_count: ', increasing_count)

        for count in range(max_t, len(hr) - 1):
            sample = [hr[count], hr[count + 1]]
            slope, intercept, r_value, p_value, std_err = linregress([0, 1], sample)
            # print(slope)
            if slope <= 0:
                end_hr = hr[count]
                end_t = count
                slope_count = slope_count + 1
                if slope == 0 and end_hr <= min_hr:
                    break
            elif np.mean(hr[min_t:max_t + 1]) <= hr[count]:
                continue
            else:
                break

            if count + 1 == len(hr) - 1:
                temp = end_hr
                end_hr = np.min([end_hr, hr[count + 1]])
                if temp != end_hr:
                    end_t = len(hr) - 1

        if end_hr == hr[end_t - 1]:
            end_t = end_t - 1
            if end_hr == hr[end_t - 1]:
                end_t = end_t - 1

        end_hr_list = hr[max_t:end_t + 1]
        end_x = []
        for count in range(0, len(end_hr_list)):
            end_x.append(count)

        if end_t == max_t and end_hr == max_hr:
            slope_down = 0
        else:
            slope_down, intercept, r_value, p_value, std_err = linregress(end_x, end_hr_list)

        print('min_hr: ', min_hr, ', min_t: ', min_t, ', max_hr: ', max_hr, ', max_t: ', max_t, ', end_hr: ', end_hr,
              ', end_t: ', end_t)

        w_up = max_t - min_t
        w_down = end_t - max_t
        h_down = max_hr - end_hr
        h = max_hr - min_hr

        new_x = []
        up_hr = []
        for count in range(min_t, max_t + 1):
            new_x.append(count - min_t)
            up_hr.append(hr[count])

        slope_up, intercept, r_value, p_value, std_err = linregress(new_x, up_hr)

        new_x = []
        down_hr = []

        for count in range(max_t, end_t + 1):
            new_x.append(count - max_t)
            down_hr.append(hr[count])

        std = np.std(hr[min_t:end_t + 1])  # during one cycle
        avg = np.mean(hr[min_t:max_t + 1])  # when hr is increasing

        print('UP')
        print('w_up: ', w_up, ', h_up: ', h, ', theta_up: ', math.atan(w_up / h), ',slope_up: ',
              slope_up)

        print('DOWN')
        if w_down == 0 and h_down == 0:
            print('w_down: ', w_down, ', h_down: ', h_down, ', theta_down: ', 0, ',slope_down: ',
                  0)
        else:
            print('w_down: ', w_down, ', h_down: ', h_down, ', theta_down: ', math.atan(w_down / h_down),
                  ',slope_down: ',
                  slope_down)

        print('OTHERS')
        print('std: ', std, 'mean: ', avg, ', peak: ', max_hr)

        plt.title(key)
        plt.plot(x, smoothing_hr)
        test = self._get_peak(smoothing_hr, key)
        plt.axvline(x=test, color='y')
        plt.show()

    def _generate_csv(self, data_path: str):
        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        writing_list = []
        writing_list.append('key')
        writing_list.append('peak')
        writing_list.append('mean')
        writing_list.append('std')
        writing_list.append('slope_up')
        writing_list.append('height_up')
        writing_list.append('width_up')
        writing_list.append('angle_up')
        writing_list.append('slope_down')
        writing_list.append('height_down')
        writing_list.append('width_down')
        writing_list.append('angle_down')
        writing_list.append('variation')
        writing_list.append('cc_avg')
        writing_list.append('cc_std')
        writing_list.append('peak_avg')
        writing_list.append('peak_std')
        writing_list.append('begin')
        writing_list.append('up_start')
        writing_list.append('max')
        writing_list.append('down_start')
        writing_list.append('end')
        writing_list.append('food_item')
        csvWrite.writerow(writing_list)

        writing_list = []
        writing_list.append(self._key)
        writing_list.append(self._peak)
        writing_list.append(self._stat['mean'])
        writing_list.append(self._stat['std'])
        writing_list.append(self._increasing_feature['slope'])
        writing_list.append(self._increasing_feature['height'])
        writing_list.append(self._increasing_feature['width'])
        writing_list.append(self._increasing_feature['tan'])
        writing_list.append(self._decreasing_feature['slope'])
        writing_list.append(self._decreasing_feature['height'])
        writing_list.append(self._decreasing_feature['width'])
        writing_list.append(self._decreasing_feature['tan'])
        writing_list.append(self._variation)
        writing_list.append(self._interval_var['cc_avg'])
        writing_list.append(self._interval_var['cc_std'])
        writing_list.append(self._interval_var['peak_avg'])
        writing_list.append(self._interval_var['peak_std'])
        writing_list.append(self._begin)
        writing_list.append(self._up_start)
        writing_list.append(self._max)
        writing_list.append(self._down_start)
        writing_list.append(self._end)
        writing_list.append(self._data[self._key]['label'])
        csvWrite.writerow(writing_list)

    def _update_csv(self, data_path: str):
        with open(data_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            writing_list = []
            for row in readCSV:
                temp = []
                for value in row:
                    temp.append(value)

                writing_list.append(temp)

        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for count in range(0, len(writing_list)):
            csvWrite.writerow(writing_list[count])

        writing_list = []
        writing_list.append(self._key)
        writing_list.append(self._peak)
        writing_list.append(self._stat['mean'])
        writing_list.append(self._stat['std'])
        writing_list.append(self._increasing_feature['slope'])
        writing_list.append(self._increasing_feature['height'])
        writing_list.append(self._increasing_feature['width'])
        writing_list.append(self._increasing_feature['tan'])
        writing_list.append(self._decreasing_feature['slope'])
        writing_list.append(self._decreasing_feature['height'])
        writing_list.append(self._decreasing_feature['width'])
        writing_list.append(self._decreasing_feature['tan'])
        writing_list.append(self._variation)
        writing_list.append(self._interval_var['cc_avg'])
        writing_list.append(self._interval_var['cc_std'])
        writing_list.append(self._interval_var['peak_avg'])
        writing_list.append(self._interval_var['peak_std'])
        writing_list.append(self._begin)
        writing_list.append(self._up_start)
        writing_list.append(self._max)
        writing_list.append(self._down_start)
        writing_list.append(self._end)
        writing_list.append(self._data[self._key]['label'])
        csvWrite.writerow(writing_list)
