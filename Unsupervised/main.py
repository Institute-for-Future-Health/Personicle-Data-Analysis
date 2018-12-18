from Experiment.Spectral import Spectral
from Experiment.girvanNewman import girvanNewman
from Experiment.kmeans import kmeans
from Experiment.makeGraph import makeGraph
from Experiment.unsupervised import unsupervised

if __name__ == "__main__":
    ###########################################
    k = 4
    algorithm = 'spectral'
    # algorithm = 'girvan_newman'
    feature_set = ['peak', 'time_to_get_max', 'mean', 'variation']
    result_file = 'data_4_sp_1213'
    cluster = 3
    #
    unsupervised = unsupervised(k, algorithm, feature_set)
    unsupervised.set_data_frame(result_file, cluster)
    unsupervised.run()

    # dataFrame = unsupervised.get_selected_subset_data()
    # length = len(dataFrame.keys())
    # numpy_array = dataFrame.as_matrix()

    # makeGraph('kneighbors', numpy_array)
    # makeGraph('radius_neighbors', numpy_array)
