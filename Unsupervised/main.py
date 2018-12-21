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
    feature_set = ['peak_avg', 'mean', 'peak']
    result_file = 'data_4_sp_1213'
    cluster = 3

    unsupervised = unsupervised(k, algorithm, feature_set)
    # unsupervised.set_data_frame(result_file, cluster)
    unsupervised.run()

    # unsupervised.draw_mod_plot_for_spectral_clustering(30)

    # dataFrame = unsupervised.get_selected_subset_data()
    # length = len(dataFrame.keys())
    # numpy_array = dataFrame.as_matrix()

    # makeGraph('kneighbors', numpy_array)
    # makeGraph('radius_neighbors', numpy_array)

    # k = 1 - -2.5383659858371268e-18
    # k = 2 - 0.44265528873494325