import csv
import datetime
import json

from variable import variable


class extractEating:

    def __init__(self, whole_data_path: str, daily_lifelog_path: str, daily_segment_path: str, date: str, data_type: int):
        if data_type == variable.whole_data:
            self._whole_data_path = whole_data_path
        elif data_type == variable.daily_data:
            self._daily_lifelog_path = daily_lifelog_path
            self._daily_segment_path = daily_segment_path
            self._date = date

        self._data_type = data_type
        self._segment_array = []
        self._lifelog_array = []

        self._preprocess()

    def _get_feature_whole(self, daily_id: str, time_window: str, feature: str):

        for value in self._lifelog_array[daily_id]['mobile']:
            time_window_list = time_window.split('_')
            key = '{}{}{}{}'.format(time_window_list[1], time_window_list[0], '_', time_window_list[2])

            if value is not None and type(value) is dict:
                if key == value['time']['timeWindow']:
                    return value[feature]
            elif value is not None and type(value) is str:
                if key == self._lifelog_array[daily_id]['mobile'][value]['time']['timeWindow']:
                    return self._lifelog_array[daily_id]['mobile'][value][feature]

        return None

    def _get_feature_daily(self, time_window: str, feature: str):

        for value in self._lifelog_array:
            time_window_list = time_window.split('_')
            key = '{}{}{}{}'.format(time_window_list[1], time_window_list[0], '_', time_window_list[2])

            if value is not None and type(value) is dict:
                if key == value['time']['timeWindow']:
                    return value[feature]
            elif value is not None and type(value) is str:
                if key == self._lifelog_array[value]['time']['timeWindow']:
                    return self._lifelog_array[value][feature]

        return None

    def _get_venue_name(self, location: dict, is_food_venue: bool):
        if is_food_venue:
            return location['topLabeledLatLngs'][0]['name']
        else:
            if 'labeledLatLngs' in location:
                for venue_name_obj in location['labeledLatLngs']:
                    # print(len(location['labeledLatLngs']), ',', venue_name_obj)
                    if 'type' in venue_name_obj and (79 in venue_name_obj['type'] or 38 in venue_name_obj['type'] or 15 in venue_name_obj['type'] or 7 in venue_name_obj['type'] or 9 in venue_name_obj['type']):
                        return venue_name_obj['name']

        return None

    def get_event(self, event: str):
        event_obj = {}

        if self._data_type == variable.whole_data:
            for daily_id in self._segment_array:
                for time_window in self._segment_array[daily_id]:
                    if type(time_window) is str and self._segment_array[daily_id][time_window]['dailyActivitySet'][0][
                        'KEY_DAILYACTIVITY'] == event \
                            and 'heartRate' in self._segment_array[daily_id][time_window] and 'step' in \
                            self._segment_array[daily_id][time_window]:
                        key = '{}{}{}'.format(daily_id, '_', time_window)
                        venue_type = self._segment_array[daily_id][time_window]['dailyActivitySet'][0]['KEY_S_L_VENUE_TYPE']
                        heart_rate = self._segment_array[daily_id][time_window]['heartRate']
                        step = self._segment_array[daily_id][time_window]['step']
                        # time = self._segment_array[daily_id][time_window]['labeledSegment'][0]['timeStamp']
                        time_list = []

                        # hour = int(time[0:time.rfind(':')])
                        # min = time[time.rfind(':') + 1:]

                        hour = int(int(key[10:13]) / 12)
                        if int(key[10:13]) % 12 == 0:
                            min = 55
                        else:
                            min = ((int(key[10:13]) % 12) - 1) * 5


                        for count in range(0, len(heart_rate)):
                            new_time = datetime.datetime(2018, 8, 6, int(hour), int(min)) + datetime.timedelta(
                                minutes=int(count))
                            new_time = "%s:%s" % (new_time.hour, new_time.minute)
                            time_list.append(new_time)

                        dataSet = {}
                        dataSet.update({'event': event})
                        dataSet.update({'venue_type': venue_type})
                        dataSet.update({'heartRate': heart_rate})
                        dataSet.update({'step': step})
                        dataSet.update({'timeStamp': time_list})

                        # if key == ''
                        if len(heart_rate) >= 30:
                            location = self._get_feature_whole(daily_id, key, 'location')

                            if location is None:
                                venue_name = self._segment_array[daily_id][time_window]['dailyActivitySet'][0][
                                    'KEY_S_L_VENUE_NAME']
                            elif venue_type != 'food' and venue_type != 'cafe' and venue_type != 'bakery' and venue_type != 'restaurant' and venue_type != 'bar':
                                venue_name = self._get_venue_name(location, False)
                            else:
                                venue_name = self._get_venue_name(location, True)

                            if '0604' in key:
                                venue_name = 'NOMO SOGO'

                            if venue_name is not None:
                                dataSet.update({'venue_name': venue_name})
                                event_obj.update({key: dataSet})
        elif self._data_type == variable.daily_data:
            for time_window in self._segment_array:
                if type(time_window) is str and self._segment_array[time_window]['dailyActivitySet'][0][
                    'KEY_DAILYACTIVITY'] == event \
                        and 'heartRate' in self._segment_array[time_window] and 'step' in \
                        self._segment_array[time_window]:
                    key = '{}{}{}'.format(self._date, '_', time_window)
                    venue_type = self._segment_array[time_window]['dailyActivitySet'][0]['KEY_S_L_VENUE_TYPE']
                    heart_rate = self._segment_array[time_window]['heartRate']
                    step = self._segment_array[time_window]['step']
                    time_list = []

                    hour = int(int(key[10:13]) / 12)
                    if int(key[10:13]) % 12 == 0:
                        min = 55
                    else:
                        min = ((int(key[10:13]) % 12) - 1) * 5

                    for count in range(0, len(heart_rate)):
                        new_time = datetime.datetime(2018, 8, 6, int(hour), int(min)) + datetime.timedelta(
                            minutes=int(count))
                        new_time = "%s:%s" % (new_time.hour, new_time.minute)
                        time_list.append(new_time)

                    dataSet = {}
                    dataSet.update({'event': event})
                    dataSet.update({'venue_type': venue_type})
                    dataSet.update({'heartRate': heart_rate})
                    dataSet.update({'step': step})
                    dataSet.update({'timeStamp': time_list})

                    location = self._get_feature_daily(key, 'location')
                    venue_name = self._get_venue_name(location, True)

                    dataSet.update({'venue_name': venue_name})
                    event_obj.update({key: dataSet})

                    # if len(heart_rate) >= 25:
                    #     location = self._get_feature_daily(key, 'location')
                    #
                    #     if location is None:
                    #         venue_name = self._segment_array[time_window]['dailyActivitySet'][0][
                    #             'KEY_S_L_VENUE_NAME']
                    #     elif venue_type != 'food' and venue_type != 'cafe' and venue_type != 'bakery' and venue_type != 'restaurant' and venue_type != 'bar' and venue_type != 'meal_takeaway':
                    #         venue_name = self._get_venue_name(location, False)
                    #     else:
                    #         venue_name = self._get_venue_name(location, True)
                    #
                    #     if venue_name is not None:
                    #         dataSet.update({'venue_name': venue_name})
                    #         event_obj.update({key: dataSet})
        return event_obj

    def get_filtered_event(self, event_obj: dict) -> dict:
        filtered_event = {}
        for obj in event_obj:
            if 'Sprouts' not in event_obj[obj]['venue_name']:
                filtered_event.update({obj: event_obj[obj]})

        return filtered_event

    def write_data(self, filtered_event: dict, name: str):
        if self._data_type == variable.whole_data:
            path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/'+name+'_segment_res_whole.csv'
        elif self._data_type == variable.daily_data:
            path = '/Users/hyungiko/Desktop/Personicle Data/eating/segment/'+name+'_segment_res_'+self._date+'.csv'

        csvWrite = csv.writer(
            open(path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        # print(filtered_event)
        if filtered_event != 'None':
            for key in filtered_event:
                event = filtered_event[key]['event']
                venue_type = filtered_event[key]['venue_type']
                venue_name = filtered_event[key]['venue_name']
                heartRate = filtered_event[key]['heartRate']
                time = filtered_event[key]['timeStamp']
                step = filtered_event[key]['step']

                for counter in range(0, len(heartRate)):
                    csvWrite.writerow([key, time[counter], heartRate[counter], step[counter], venue_type,
                                       venue_name, event])

    def _preprocess(self):
        if self._data_type == variable.whole_data:
            total = json.load(open(self._whole_data_path))

            self._lifelog_array = total['lifeLog']
            self._segment_array = total['segment']
        elif self._data_type == variable.daily_data:
            self._lifelog_array = json.load(open(self._daily_lifelog_path))['mobile']
            self._segment_array = json.load(open(self._daily_segment_path))
            print('')
