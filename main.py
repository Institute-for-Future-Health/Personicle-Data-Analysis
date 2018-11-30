import numpy as np
from numpy.distutils.system_info import p
from sklearn.cluster import SpectralClustering

from Experiment.globalVariable import global_variable
from Experiment.spectralClustering import spectralClustering
from Experiment.unsupervised import unsupervised

if __name__ == "__main__":

    ###########################################
    k = 4
    unsupervised = unsupervised()

    dataFrame = unsupervised.get_selected_subset_data()

    numpy_array = dataFrame.as_matrix()
    clustering = SpectralClustering(n_clusters=k, affinity='nearest_neighbors', n_init=10).fit_predict(numpy_array)
    # # # clustering = SpectralClustering(n_clusters=5, assign_labels = "discretize", random_state = 0).fit(numpy_array)
    label = clustering
    unsupervised.set_label(label, k)
    unsupervised.generate_csv()
    print(clustering)

    dataFrame.insert(len(dataFrame.keys()), 'label', clustering)
    dataFrame = dataFrame.sort_values(by=['label'])
    selected_fature = dataFrame.iloc[:, 0:5]

    import seaborn as sns;
    sns.set()
    xticks = selected_fature.keys()
    # yticks = unsupervised.get_selected_feature(global_variable.food_item)

    ax = sns.heatmap(selected_fature, cmap="YlGnBu", xticklabels=xticks)

    import matplotlib.pyplot as plt
    plt.show()

