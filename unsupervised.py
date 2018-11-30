import csv

import numpy as np
import networkx as nx

from Experiment.featureSelection import feature_selection
from Experiment.globalVariable import global_variable
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans, AffinityPropagation, MeanShift

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

    def __init__(self):
        # self._norm_method = norm_method
        self._feature_selection = feature_selection()
        self._feature_selection.normalize()
        self._label = []
        self._feature_list = []
        self._k = 0

    def get_selected_subset_data(self):
        return self._feature_selection.get_features()

    def get_selected_feature(self, key):
        return self._feature_selection.get_selected_feature(key)

    def get_all_data(self):
        return self._feature_selection.get_all_feature()

    def k_means(self, feature_list: list, k: int):
        self._k = k
        self._feature_list = feature_list

        X = self._feature_selection.get_features()
        X = X.as_matrix()
        # _elbow_plot(X)

        kmeans = KMeans(n_clusters=self._k)
        # Fitting the input data
        kmeans = kmeans.fit(X)
        # Getting the cluster labels
        self._label = kmeans.predict(X)
        # Centroid values
        centroids = kmeans.cluster_centers_

        # if len(feature_list) < 10:
        #     import matplotlib.pyplot as plt
        #     for i in range(self._k):
        #         points = np.array([X[j] for j in range(len(X)) if self._label[j] == i])
        #         plt.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        #         plt.scatter(centroids[i][0], centroids[i][1], marker='*', s=200, c=colors[i])
        #
        #     plt.show()

    def _return_input(self, feature_list: list):
        if len(feature_list) == 2:
            f1 = self._feature_selection.get_selected_feature(feature_list[0])
            f2 = self._feature_selection.get_selected_feature(feature_list[1])
            return np.array(list(zip(f1, f2)))
        elif len(feature_list) == 3:
            f1 = self._feature_selection.get_selected_feature(feature_list[0])
            f2 = self._feature_selection.get_selected_feature(feature_list[1])
            f3 = self._feature_selection.get_selected_feature(feature_list[2])
            return np.array(list(zip(f1, f2, f3)))
        elif len(feature_list) == 4:
            f1 = self._feature_selection.get_selected_feature(feature_list[0])
            f2 = self._feature_selection.get_selected_feature(feature_list[1])
            f3 = self._feature_selection.get_selected_feature(feature_list[2])
            f4 = self._feature_selection.get_selected_feature(feature_list[3])
            return np.array(list(zip(f1, f2, f3, f4)))
        elif len(feature_list) == 5:
            f1 = self._feature_selection.get_selected_feature(feature_list[0])
            f2 = self._feature_selection.get_selected_feature(feature_list[1])
            f3 = self._feature_selection.get_selected_feature(feature_list[2])
            f4 = self._feature_selection.get_selected_feature(feature_list[3])
            f5 = self._feature_selection.get_selected_feature(feature_list[4])
            return np.array(list(zip(f1, f2, f3, f4, f5)))
        elif len(feature_list) == 8:
            f1 = self._feature_selection.get_selected_feature(feature_list[0])
            f2 = self._feature_selection.get_selected_feature(feature_list[1])
            f3 = self._feature_selection.get_selected_feature(feature_list[2])
            f4 = self._feature_selection.get_selected_feature(feature_list[3])
            f5 = self._feature_selection.get_selected_feature(feature_list[4])
            f6 = self._feature_selection.get_selected_feature(feature_list[5])
            f7 = self._feature_selection.get_selected_feature(feature_list[6])
            f8 = self._feature_selection.get_selected_feature(feature_list[7])
            return np.array(list(zip(f1, f2, f3, f4, f5, f6, f7, f8)))

    def set_label(self, lable: list, k: int):
        self._label = lable
        self._k = k

    def generate_csv(self):
        # name = ''
        # for value in self._feature_list:
        #     name += value

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

    def _get_num_of_pca_components(self, feature_list: list) -> int:

        from sklearn.decomposition import PCA

        # Kaiser’s stopping rule
        if self._norm_method == global_variable.pca:
            original_X = self._return_input(feature_list)
            pca = PCA(n_components=len(feature_list))
            pca.fit_transform(original_X)
            count = 0
            for item in pca.explained_variance_:
                if item > 1:
                    count += 1

            print(pca.explained_variance_)
            print(count)

        return count

    def affinity_propagation(self, feature_list: list):
        num_of_components = self._get_num_of_pca_components(feature_list)
        self._feature_list = feature_list

        X = self._return_input(feature_list)

        if self._norm_method == global_variable.pca:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=num_of_components)
            X = pca.fit_transform(X)

        af = AffinityPropagation(preference=-50).fit(X)
        cluster_centers_indices = af.cluster_centers_indices_
        labels = af.labels_

        no_clusters = len(cluster_centers_indices)

        self._k = no_clusters
        print('Estimated number of clusters: %d' % no_clusters)
        self._label = labels

    def mean_shift(self, feature_list: list):
        num_of_components = self._get_num_of_pca_components(feature_list)
        self._feature_list = feature_list

        X = self._return_input(feature_list)
        if self._norm_method == global_variable.pca:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=num_of_components)
            X = pca.fit_transform(X)

        clustering = MeanShift(bandwidth=2.1).fit(X)

        self._label = clustering.labels_
        self._k = len(set(self._label))

    def agglomerative(self, feature_list: list):
        num_of_components = self._get_num_of_pca_components(feature_list)
        self._feature_list = feature_list

        X = self._return_input(feature_list)
        if self._norm_method == global_variable.pca:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=num_of_components)
            X = pca.fit_transform(X)

        clustering = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
        clustering.fit_predict(X)
        self._label = clustering.labels_
        self._k = len(set(self._label))