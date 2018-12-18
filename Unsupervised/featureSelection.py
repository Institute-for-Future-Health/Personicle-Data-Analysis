import pandas as pd

from sklearn import preprocessing


def get_all_data():
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/all_data.csv'
    df = pd.io.parsers.read_csv(data_path)

    return df


def get_clustering_result(file_name: str):
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/result/' + file_name + '.csv'
    df = pd.io.parsers.read_csv(data_path)

    return df


class feature_selection:
    def __init__(self):
        self._data_frame = get_all_data()
        self._original_df = self._data_frame
        self._feature_set = []

    def get_cluster(self, file_name: str, k: int):
        self._data_frame = get_clustering_result(file_name)
        return self._data_frame[str(k)].values

    def get_selected_feature(self, key: str):
        return self._original_df[key].values

    def get_all_feature(self):
        return self._original_df

    def set_original_df(self, data_frame):
        self._original_df = data_frame

    def get_data_frame(self):
        return self._data_frame

    def set_features(self, feature_set: list):
        self._feature_set = feature_set

    def get_features(self):
        return self._feature_set

    def set_data_frame(self, dataframe):
        self._data_frame = dataframe

    def normalize(self):
        if len(self._feature_set) == 0:
            print('feature-set is empty')
            return

        min_max_scaler = preprocessing.MinMaxScaler()

        self._original_df = self._data_frame
        self._data_frame = self._data_frame[self._feature_set]

        np_scaled = min_max_scaler.fit_transform(self._data_frame)

        count = 0
        df_normalized = pd.DataFrame(np_scaled)
        key_array = []
        for key in list(self._data_frame.columns.values):
            if key != 'food_item':
                self._data_frame[key] = df_normalized[count]
                key_array.append(key)
            count += 1

        test = self._data_frame