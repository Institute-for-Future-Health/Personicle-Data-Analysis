import csv

from sklearn.neighbors import kneighbors_graph, radius_neighbors_graph


class makeGraph:
    def __init__(self, graph_type: str, m_input: list):
        if graph_type == 'kneighbors':
            self._connectivity = kneighbors_graph(m_input, n_neighbors=15,
                                            p=1,
                                            include_self=True,
                                            n_jobs=None)
        elif graph_type == 'radius_neighbors':
            self._connectivity = radius_neighbors_graph(m_input, 1.5, mode='connectivity',
                                       p=2)

        self._make_graph()

    def _make_graph(self):
        # radius_neighbors_graph
        test = self._connectivity.toarray()

        data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/sample2.txt'
        csvWrite = csv.writer(
            open(data_path, 'w'),
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        count = 0
        for value in test:
            g = [i for i, e in enumerate(value) if e == 1]
            for value2 in g:
                writing_list = [str(count) + ' ' + str(value2)]
                csvWrite.writerow(writing_list)
            count += 1

        print('graph done')