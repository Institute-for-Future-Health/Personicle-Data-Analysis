import csv

import numpy as np
# import pd as pd
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def get_data() -> dict:
    data_path = '/Users/hyungiko/Desktop/Personicle Data/eating/dataset/all_data.csv'

    peak = []
    mean = []
    std = []
    slope_up = []
    height_up = []
    width_up = []
    angle_up = []
    variation = []

    with open(data_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if 'key' not in row:
                peak.append(float(row[1]))
                mean.append(float(row[2]))
                std.append(float(row[3]))
                slope_up.append(float(row[4]))
                height_up.append(float(row[5]))
                width_up.append(float(row[6]))
                angle_up.append(float(row[7]))
                variation.append(float((row[12])))

    _data = {}
    _data.update({'peak': peak})
    _data.update({'mean': mean})
    _data.update({'std': std})
    _data.update({'slope_up': slope_up})
    _data.update({'height_up': height_up})
    _data.update({'width_up': width_up})
    _data.update({'angle_up': angle_up})
    _data.update({'variation': variation})

    return _data


if __name__ == "__main__":
    _data = get_data()

    peak = np.array(_data['peak']).reshape(-1, 1)
    mean = np.array(_data['mean']).reshape(-1, 1)
    std = np.array(_data['std']).reshape(-1, 1)
    slope_up = np.array(_data['slope_up']).reshape(-1, 1)
    height_up = np.array(_data['height_up']).reshape(-1, 1)
    height_up = np.array(_data['height_up']).reshape(-1, 1)
    width_up = np.array(_data['width_up']).reshape(-1, 1)
    angle_up = np.array(_data['angle_up']).reshape(-1, 1)
    variation = np.array(_data['variation']).reshape(-1, 1)

    peak = StandardScaler().fit_transform(peak)
    mean = StandardScaler().fit_transform(mean)
    std = StandardScaler().fit_transform(std)
    slope_up = StandardScaler().fit_transform(slope_up)
    height_up = StandardScaler().fit_transform(height_up)
    width_up = StandardScaler().fit_transform(width_up)
    angle_up = StandardScaler().fit_transform(angle_up)
    variation = StandardScaler().fit_transform(variation)

    row = []
    for count in range(0, len(peak)):
        temp = []
        temp.append(peak[count][0])
        temp.append(mean[count][0])
        temp.append(std[count][0])
        temp.append(slope_up[count][0])
        temp.append(height_up[count][0])
        temp.append(width_up[count][0])
        temp.append(angle_up[count][0])
        temp.append(variation[count][0])

        row.append(temp)

    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(row)

    # sse = {}
    # for k in range(1,10):
    #     kmeans = KMeans(n_clusters=k, max_iter=1000).fit(principalComponents)
    #     sse[k] = kmeans.inertia_
    #
    # plt.figure()
    # plt.plot(list(sse.keys()), list(sse.values()))
    # plt.xlabel("Number of cluster")
    # plt.ylabel("SSE")
    # plt.show()


    kmeans = KMeans(n_clusters=4)
    # Fitting with inputs
    kmeans = kmeans.fit(principalComponents)
    # Predicting the clusters
    labels = kmeans.predict(principalComponents)
    # Getting the cluster centers
    C = kmeans.cluster_centers_
    #
    # X = principalComponents
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels)
    # ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker='*', c='#050505', s=1000)

    # fig.show()
    # print(labels)
    for value in labels:
        print(value)
    # plt.scatter([0, 0, 1], [1, 0, 1], [0, 1, 1], c='black')
    # plt.show()
    # for value in principalComponents:
    #     print(value)
    # principalDf = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2', 'principal component 3'])
    # print(principalComponents)
