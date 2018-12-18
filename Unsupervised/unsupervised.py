import csv
import itertools
import operator

import numpy as np
import networkx as nx
from networkx.algorithms.community import girvan_newman
from sklearn.utils import shuffle

from Experiment.featureSelection import feature_selection
from Experiment.globalVariable import global_variable
from sklearn.cluster import KMeans, SpectralClustering

from Experiment.makeGraph import makeGraph

colors = ['r', 'g', 'b', 'y', 'c', 'm']


def _elbow_plot(input: list):
    sse = {}
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k)
        kmeans = kmeans.fit(input)
        sse[k] = kmeans.inertia_

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.show()


class unsupervised:

    def __init__(self, k: int, algorithm: str, feature_set: list):
        self._k = k
        self._algorithm = algorithm
        self._feature_selection = feature_selection()
        self._feature_selection.set_features(feature_set)
        self._feature_selection.normalize()
        self._label = []
        self._feature_list = []
        self._dataFrame = self.get_selected_subset_data()

    def run(self):
        result_sample = {}
        for index in range(0, self._k):
            result_sample.update({index: ''})

        length = len(self._dataFrame.keys())
        numpy_array = self._dataFrame.as_matrix()

        if self._algorithm == 'spectral':
            label = self._spectral_clustering(numpy_array)
        elif self._algorithm == 'girvan_newman':
            makeGraph('kneighbors', numpy_array)
            label = self._girvan_newman()
        elif self._algorithm == 'kmeans':
            label = self._kmeans(numpy_array)
        else:
            print('not available algorithm')
            return

        self.set_label(label, self._k)

        count = 0
        for value in label:
            if result_sample[value] == '':
                result_sample[value] = self._dataFrame.get_value(self._dataFrame.index[count], 'peak')
            count += 1

        result_sample = sorted(result_sample.items(), key=operator.itemgetter(1))
        new_label = {}
        count = 0
        for value in result_sample:
            new_label.update({value[0]: count})
            count += 1

        count = 0
        index = []
        for value in label:
            label[count] = new_label[value]
            index.append(self._dataFrame.index[count])
            count += 1

        self.generate_csv()
        self._dataFrame.insert(len(self._dataFrame.keys()), 'label', label)
        self._dataFrame.insert(len(self._dataFrame.keys()), 'index', index)
        dataFrame = self._dataFrame.sort_values(by=['label'])

        selected_fature = dataFrame.iloc[:, 0:length]

        import seaborn as sns;

        sns.set()
        xticks = selected_fature.keys()
        # yticks = self._unsupervised.get_selected_feature(global_variable.food_item)

        ax = sns.heatmap(selected_fature, cmap="YlGnBu", xticklabels=xticks)

        for tick_label in ax.axes.get_yticklabels():
            tick_text = tick_label.get_text()
            selected_label = int(dataFrame.query('index == ' + tick_text).iloc[0]['label'])
            if selected_label == 0:
                tick_label.set_color('g')
            elif selected_label == 1:
                tick_label.set_color('b')
            elif selected_label == 2:
                tick_label.set_color('y')
            elif selected_label == 3:
                tick_label.set_color('r')
            else:
                tick_label.set_color('c')

        import matplotlib.pyplot as plt

        plt.show()

    def _spectral_clustering(self, numpy_array: list) -> list:
        clustering = SpectralClustering(n_clusters=self._k, affinity='nearest_neighbors', n_init=15).fit_predict(
            numpy_array)

        return clustering

    def _girvan_newman(self) -> list:
        k = self._k - 1

        G = nx.read_edgelist(global_variable.graph_path)
        comp = girvan_newman(G)
        result = ()
        for communities in itertools.islice(comp, k):
            result = tuple(sorted(c) for c in communities)
            print(tuple(sorted(c) for c in communities))

        food_item = self.get_selected_feature(global_variable.food_item)
        label = []
        for value in range(0, len(food_item)):
            label.append(0)

        count = 0
        for value in result:
            for index in value:
                label[int(index)] = count

            count += 1

        return label

    def _kmeans(self, numpy_array: list) -> list:
        kmeans = KMeans(n_clusters=self._k)
        # Fitting the input data
        kmeans = kmeans.fit(numpy_array)
        # Getting the cluster labels
        label = kmeans.predict(numpy_array)
        return label

    def get_selected_subset_data(self):
        return self._feature_selection.get_data_frame()

    def get_selected_feature(self, key):
        return self._feature_selection.get_selected_feature(key)

    def get_all_data(self):
        return self._feature_selection.get_all_feature()

    def set_data_frame(self, file_name: str, cluster: int):
        length = len(self._dataFrame.values)
        original_df = self._feature_selection.get_all_feature()
        data_in_cluster = self._feature_selection.get_cluster(file_name, cluster)
        index = []
        for value in data_in_cluster:
            if str(value) != 'nan':
                index.append(int(value.split(' ')[0]))

        for value in range(0, length):
            row = length - value - 1
            if row not in index:
                self._dataFrame = self._dataFrame.drop(self._dataFrame.index[row])
                original_df = original_df.drop(original_df.index[row])

        self._feature_selection.set_data_frame(self._dataFrame)
        self._feature_selection.set_original_df(original_df)

        # self._dataFrame = self.get_selected_subset_data()

    def set_label(self, lable: list, k: int):
        self._label = lable
        self._k = k

    def generate_csv(self):
        food_item = self._feature_selection.get_selected_feature(global_variable.food_item)
        unique_label = set(self._label)

        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/result/data_' + str(
            self._k) + '.csv'
        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        attr_list = []
        for value in unique_label:
            attr_list.append(value)

        csvWrite.writerow(attr_list)
        food_item_dict = {}
        max_length = 0
        for i in range(self._k):
            points = np.array([food_item[j] for j in range(len(food_item)) if self._label[j] == i])
            food_item_dict.update({i: points})
            max_length = max(max_length, len(points))

        for i in range(0, max_length + 1):
            attr_list = []
            for label in unique_label:
                if len(food_item_dict[label]) > i:
                    attr_list.append(food_item_dict[label][i])
                else:
                    attr_list.append('')

            csvWrite.writerow(attr_list)
