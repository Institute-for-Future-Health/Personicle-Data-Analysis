import itertools
import operator

import networkx as nx
from networkx.algorithms.community import girvan_newman

from Experiment.globalVariable import global_variable
from Experiment.unsupervised import unsupervised


class girvanNewman:
    def __init__(self, unsupervised: unsupervised, k: int):
        self._unsupervised = unsupervised
        self._k = k

    def run(self):
        result_sample = {}
        for index in range(0, self._k):
            result_sample.update({index: ''})

        dataFrame = self._unsupervised.get_selected_subset_data()
        length = len(self._unsupervised.get_selected_subset_data().keys())

        self._k = self._k - 1

        G = nx.read_edgelist(global_variable.graph_path)
        comp = girvan_newman(G)
        result = ()
        for communities in itertools.islice(comp, self._k):
            result = tuple(sorted(c) for c in communities)
            print(tuple(sorted(c) for c in communities))

        food_item = self._unsupervised.get_selected_feature(global_variable.food_item)
        label = []
        for value in range(0, len(food_item)):
            label.append(0)

        count = 0
        for value in result:
            for index in value:
                label[int(index)] = count

            count += 1

        self._unsupervised.set_label(label, self._k + 1)

        count = 0
        for value in label:
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
        for value in label:
            label[count] = new_label[value]
            index.append(count)
            count += 1

        self._unsupervised.generate_csv()

        dataFrame.insert(len(dataFrame.keys()), 'label', label)
        dataFrame.insert(len(dataFrame.keys()), 'index', index)
        dataFrame = dataFrame.sort_values(by=['label'])
        selected_fature = dataFrame.iloc[:, 0:length]

        import seaborn as sns;

        sns.set()
        xticks = selected_fature.keys()
        # yticks = unsupervised.get_selected_feature(global_variable.food_item)

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
            else:
                tick_label.set_color('r')

        import matplotlib.pyplot as plt

        plt.show()

