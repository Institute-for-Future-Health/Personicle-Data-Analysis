import operator

from sklearn.cluster import SpectralClustering
from sklearn.utils import shuffle

from Experiment.unsupervised import unsupervised


class Spectral:
    def __init__(self, k: int):
        self._k = k
        self._unsupervised = unsupervised()

    def run(self):
        result_sample = {}
        for index in range(0, self._k):
            result_sample.update({index: ''})

        dataFrame = self._unsupervised.get_selected_subset_data()
        length = len(dataFrame.keys())
        numpy_array = dataFrame.as_matrix()

        clustering = SpectralClustering(n_clusters=self._k, affinity='nearest_neighbors', n_init=11).fit_predict(
            numpy_array)

        label = clustering
        self._unsupervised.set_label(label, self._k)

        count = 0
        for value in clustering:
            if result_sample[value] == '':
                result_sample[value] = dataFrame.get_value(count, 'peak')
            count += 1

        result_sample = sorted(result_sample.items(), key=operator.itemgetter(1))
        new_label = {}
        count = 0
        for value in result_sample:
            new_label.update({value[0]: count})
            count += 1

        count = 0
        index = []
        for value in clustering:
            clustering[count] = new_label[value]
            index.append(count)
            count += 1

        self._unsupervised.generate_csv()
        dataFrame.insert(len(dataFrame.keys()), 'label', clustering)
        dataFrame.insert(len(dataFrame.keys()), 'index', index)
        dataFrame = dataFrame.sort_values(by=['label'])

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
