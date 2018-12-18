import json

import numpy as np

jordan_except_these_date = ['0805_2018', '0804_2018', '0729_2018', '0728_2018', '0727_2018', '0718_2018', '0716_2018',
                            '0715_2018',
                            '0711_2018', '0709_2018', '0708_2018', '0707_2018', '0701_0218', '0630_2018', '0629_2018',
                            '0728_2018',
                            '0627_2018', '0626_2018', '0625_2018', '0624_2018', '0623_2018', '0619_2018', '0618_2018',
                            '0617_2018',
                            '0610_2018', '0609_2018', '0608_2018', '0607_2018', '0606_2018', '0605_2018', '0604_2018',
                            '0602_2018',
                            '0522_2018', '0521_2018', '0520_2018', '0428_2018', '0424_2018', '0325_2018']

moving_activity = ['going', 'shopping', 'commuting', 'exercising', 'sleep', 'using toilet']


class SAX:
    def __init__(self, data_path: str):
        self._data_path = data_path
        self._get_data()
        # self._get_hr = []

    def _get_data(self):
        total = json.load(open(self._data_path))['segment']
        self._heart_rate = []
        for date in total:
            if date not in jordan_except_these_date:
                daily_activity_set = total[date]
                for time_window in daily_activity_set:
                    daily_activity = daily_activity_set[time_window]['dailyActivitySet'][0]['KEY_DAILYACTIVITY']
                    if 'heartRate' in daily_activity_set[time_window] and 'step' in daily_activity_set[time_window]:
                        heart_rate = daily_activity_set[time_window]['heartRate']
                        step = daily_activity_set[time_window]['step']
                        if daily_activity not in moving_activity:
                            for count in range(0, len(step)):
                                if step[count] == 0:
                                    self._heart_rate.append(heart_rate[count])

        sd_hr = np.std(np.array(self._heart_rate))
        mean_hr = np.mean(np.array(self._heart_rate))

        print('Std: ', sd_hr, ', mean: ', mean_hr)
