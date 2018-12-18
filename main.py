# from explore_eating import exploreEating
import csv
import math

import networkx as nx
from networkx.algorithms.community import girvan_newman
from numpy.core.umath import degrees

from Experiment.structuralFeature import structuralFeature
from SAX import SAX
from extractEating import extractEating
from segment import segment
from Data.eating_label import eating_label
from splitData import splitData
from variable import variable
from dualSegment import dualSegment

fileName = ''
date = ''
userName = ''


def generate_restaurant_eating_csv_using_daily_segment(data_type: int):
    if data_type == variable.daily_data:
        file_name = 'personicle-1498515264813-' + date + '-export'

        # daily data
        segment_path = '/Users/hyungiko/Desktop/Personicle Data/json/daily/'+userName+'/' + file_name + '.json'
        lifelog_path = '/Users/hyungiko/Desktop/Personicle Data/json/daily/'+userName+'/lifelog/' + file_name + '.json'

        extract_eating = extractEating('', lifelog_path, segment_path, date, data_type)
        filtered_event = extract_eating.get_filtered_event(extract_eating.get_event('eating'))

        get_segment = segment('', '', '')
        path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/' + userName + '_segment_res_' + date + '.csv'

        get_segment.get_segment_res(filtered_event, path)

        # extract_eating.write_data(filtered_event, userName)

    elif data_type == variable.whole_data:
        # whole data
        whole_path = '/Users/hyungiko/Desktop/Personicle Data/json/whole/' + fileName + '.json'

        extract_eating = extractEating(whole_path, '', '', '', data_type)
        filtered_event = extract_eating.get_filtered_event(extract_eating.get_event('eating'))
        extract_eating.write_data(filtered_event, userName)


def test():
    csv_path = '/Users/hyungiko/Desktop/Personicle Data/eating/eating_' + userName + '.csv'

    csv_path = '/Users/hyungiko/Desktop/Personicle Data/Jordan/symbolicResultHomeEvent.csv'
    # explore_eating = exploreEating(csv_path)
    # explore_eating.test()
    # sample_set = explore_eating.get_sample_set()
    # explore_eating.draw_the_highest_hr_plot(sample_set)


def generate_restaurant_eating_csv():
    data_path = '/Users/hyungiko/Desktop/Personicle Data/json/whole/' + fileName + '.json'

    get_segment = segment(data_path, userName, '')
    get_segment.get_segment()
    # get_segment


# Segment를 daily로 다운받았을 때, 이 함수 사용 => Segmentation + CSV file 만들어 줌
def generate_non_restaurant_eating_csv_using_daily_segment():
    # date = '1020_2018'
    fileName = 'personicle-1498515264813-' + date + '-export'
    # userName2 = userName + '_' + date
    data_path = '/Users/hyungiko/Desktop/Personicle Data/json/daily/'+userName+'/' + fileName + '.json'

    get_segment = segment(data_path, userName + '_' + date, date)
    get_segment.get_segment()


# Eating Segment를 전체 데이터에서 찾아 새로운 CSV 파일을 만들어 줌
def generate_eating_labeled_segemt(type: str):
    get_eating_label = eating_label(userName)
    get_eating_label.get_eating_label(type)
    get_eating_label.combine_eating()


def get_eating_sub_segment(data_type: int):
    # userName = 'jordan2'
    attributes = ['time_window', 'time_stamp', 'heart_rate', 'step', 'label', 'meal_type']

    if variable.restaurant == data_type:
        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/eatingLabel/eating_res_whole_' + userName + '.csv'
    elif variable.home:
        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/eatingLabel/' + userName + '_label.csv'

    dualSegment(data_path, attributes, data_type, userName)


def split_data():
    attributes = ['time_window', 'time_stamp', 'heart_rate', 'step', 'segment_type', 'meal_type', 'label',
                  'symbolic_heart_rate']
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/dualSegment_res.csv'
    splitData(data_path, attributes, 'restaurant')

    attributes = ['time_window', 'time_stamp', 'heart_rate', 'step', 'label', 'meal_type', 'symbolic_heart_rate']
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/dualSegment_home.csv'
    splitData(data_path, attributes, 'home')


def set_variable():
    if userName == 'jordan2':
        fileName = 'personicle-1498515264813-00000000-28e4-7fe3-ffff-ffff8d49054a-export'

    # Jordan1
    # fileName = 'personicle-1498515264813-ffffffff-963d-b101-5969-03af624ade3c-export'
    # Jordan2

    # Ramesh
    # fileName = 'personicle-1498515264813-ffffffff-f59c-af93-ffff-ffffc40892f8-export'
    # Pooya
    # fileName = 'personicle-1498515264813-ffffffff-8d8e-861c-796c-0e464957ef67-export'
    # Heena
    # fileName = 'personicle-1498515264813-00000000-4a39-6bb5-e3cc-bedb58667e97-export'


def get_dataset_seprately(path: str, result: list) -> list:
    with open(path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if 'key' not in row:
                result.append(row)

    return result


def combine_all_dataset():
    result = []
    get_dataset_seprately('/Users/hyungiko/Desktop/Personicle Data/eating/dataset/restaurant_data.csv', result)
    get_dataset_seprately('/Users/hyungiko/Desktop/Personicle Data/eating/dataset/lunch_home_data.csv', result)
    get_dataset_seprately('/Users/hyungiko/Desktop/Personicle Data/eating/dataset/dinner_home_data.csv', result)
    get_dataset_seprately('/Users/hyungiko/Desktop/Personicle Data/eating/dataset/breakfast_home_data.csv', result)

    csvWrite = csv.writer(
        open('/Users/hyungiko/Desktop/Personicle Data/eating/dataset/all_data.csv', 'w'),
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    column = ['key', 'peak', 'mean', 'std', 'slope_up', 'height_up', 'width_up', 'angle_up', 'slope_down',
              'height_down', 'width_down', 'angle_down', 'variation', 'cc_avg', 'cc_std', 'peak_avg', 'peak_std',
              'begin', 'up_start', 'max', 'down_start', 'end', 'time_to_get_max',
              'food_item']

    csvWrite.writerow(column)

    count = 0
    for row in result:
        row[len(row)-1] = str(count) + ' ' + row[len(row)-1]

        # max_percentile = str((float(row[19]) - float(row[17])) / (float(row[21]) - float(row[17])))
        # row.insert(len(row)-1, max_percentile)
        row.insert(len(row)-1, float(row[19]) - float(row[17]))

        csvWrite.writerow(row)
        count += 1


###########################################################################
# How to update food log
# 1. download daily segment table from Firebase
# 2. Copy the file to /json/daily
# 3. Run generate_non_restaurant_eating_csv_using_daily_segment()
# 3-1. You need to set date to the target date
# 3-2. Copy generated file's sampleset to jordan2_segment.csv
# 4. Update both google sheet and /foodLog/jordan2_foodLog
# 4-1. Confirm the logging time from jordan2_segment.csv
# 5. Run generate_eating_labeled_segemt()
# 6. Run get_eating_sub_segment(variable.home)
# 7. Run split_data()


if __name__ == "__main__":
    date = '1212_2018'
    data_type = variable.daily_data
    userName = 'jordan2'
    # userName = 'kevin'

    set_variable()

    ###########################################################################
    # if you want to get restaurant eating data --> call 'get_restaurant_eating'
    # 1. get_restaurant_eating(variable.daily_data) --> daily data
    # 2. get_restaurant_eating(variable.whole_data) --> whole data

    # generate_restaurant_eating_csv_using_daily_segment(data_type)
    # get_restaurant_eating(variable.whole_data)

    # generate_eating_labeled_segemt('restaurant')
    ###########################################################################

    ###########################################################################
    # if you want to get home eating data
    # 1. call 'generate_non_restaurant_eating_csv_using_daily_segment' to get raw data
    # 1-1. update foodLog.csv
    # 2. and then call 'generate_eating_labeled_segment' to get eating label from the raw data

    # generate_non_restaurant_eating_csv_using_daily_segment()
    # generate_eating_labeled_segemt('home')

    ###########################################################################

    ###########################################################################
    # Dual Segmentation
    # get_eating_sub_segment(variable.home)

    ###########################################################################

    ###########################################################################
    # Split data into Breakfast, Lunch, and Dinner
    # split_data()
    ###########################################################################

    ###########################################################################
    # Get Structural Features
    structuralFeature()

    ###########################################################################
    # Combine all data
    # combine_all_dataset()
