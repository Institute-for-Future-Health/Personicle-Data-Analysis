import pandas as pd

from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from Experiment.PFA import PFA
import numpy.matlib
import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import rbf_kernel
from numpy import linalg as LA
from Experiment.SPEC import SPEC, NormalizedCut
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans


def get_data():
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/all_data.csv'
    df = pd.io.parsers.read_csv(data_path)

    return df


class feature_selection:
    def __init__(self):
        self._data_frame = get_data()
        self._original_df = self._data_frame

    def get_selected_feature(self, key: str):
        return self._original_df[key].values

    def get_all_feature(self):
        return self._original_df

    def get_features(self):
        return self._data_frame

    def _get_num_of_pca_components(self) -> int:

        from sklearn.decomposition import PCA

        # Kaiser’s stopping rule
        pca = PCA(n_components=len(self._data_frame.columns))
        pca.fit_transform(self._data_frame)
        count = 0
        for item in pca.explained_variance_:
            if item > 1:
                count += 1

        print(pca.explained_variance_)
        print(count)

        return count

    def normalize(self):
        min_max_scaler = preprocessing.MinMaxScaler()
        # self._data_frame = self._data_frame.iloc[:, 1:17]

        self._original_df = self._data_frame
        # self._data_frame = self._data_frame[['peak', 'mean', 'std', 'slope_up', 'height_up', 'width_up', 'angle_up', 'variation', 'cc_avg', 'cc_std', 'peak_avg', 'peak_std']]
        # self._data_frame = self._data_frame[['peak_avg', 'peak_std', 'cc_avg', 'cc_std', 'variation', 'mean', 'peak', 'width_up']]
        self._data_frame = self._data_frame[['peak_avg', 'variation', 'mean', 'peak', 'width_up']]

        np_scaled = min_max_scaler.fit_transform(self._data_frame)

        count = 0
        df_normalized = pd.DataFrame(np_scaled)
        key_array = []
        for key in list(self._data_frame.columns.values):
            if key != 'food_item':
                self._data_frame[key] = df_normalized[count]
                key_array.append(key)
            count += 1

        # self._get_num_of_pca_components()
        # numpy_array = self._data_frame.as_matrix()

        # pipeline = Pipeline([
        #     ('select', NormalizedCut(3)),
        #     ('cluster', KMeans())
        # ])
        # result = pipeline.fit_predict(numpy_array)

        # spec = SPEC()
        # result= spec._calc_scores(numpy_array)
        # print('')
        # test = self.feature_ranking(self.spec(numpy_array))
        # print(len(test))
        # self._get_num_of_pca_components()
        # if method == global_variable.simple_sampling:
        #     for key in list(self._data_frame.columns.values):
        #         if key != 'key' and key != 'food_item':
        #             self._data_frame[key] = self._data_frame[key] / self._data_frame[key].max()
        #
        # elif method == global_variable.min_max:
        #     for key in list(self._data_frame.columns.values):
        #         if key != 'key' and key != 'food_item':
        #             self._data_frame[key] = (self._data_frame[key] - self._data_frame[key].min()) / (
        #                     self._data_frame[key].max() - self._data_frame[key].min())
        #
        # elif method == global_variable.z_score:
        #     for key in list(self._data_frame.columns.values):
        #         if key != 'key' and key != 'food_item':
        #             self._data_frame[key] = (self._data_frame[key] - self._data_frame[key].mean()) / self._data_frame[
        #                 key].std()
        # elif method == global_variable.pca:
        #     from sklearn.preprocessing import StandardScaler
        #     for key in list(self._data_frame.columns.values):
        #         if key != 'key' and key != 'food_item':
        #             self._data_frame[key] = StandardScaler().fit_transform(self._data_frame[key].values.reshape(-1, 1))
