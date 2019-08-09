import os
import math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

def find_vector(subdirect, filename):
    vec = list()
    data = pd.read_csv(os.path.join(subdirect, filename))
    # print(subdirect)
    X = data['posX'].values[0:30000:1000]
    Y = data['posZ'].values[0:30000:1000]
    if len(X) != 30 or len(Y) != 30:
        # false/terminate
        return vec

    # plt.scatter(X, Y)
    # plt.show()

    for x in X:
        vec.append(x)
    for y in Y:
        # print(y)
        vec.append(y)
    # print(vec)
    # quit()
    return vec


rootdir = os.getcwd()
arr = list()

# dictionary
row_dict = list()

# hardcord
SUBDIRECT = None

count = 0
# actual processing files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if '.csv' in file:
            #quit()

            # ONE TIME THING
            if not SUBDIRECT:
                SUBDIRECT = subdir

            tmp = find_vector(subdir, file)
            if not tmp:
                print('Invalid file (for this decimation strategy): ', file)
                continue
            arr.append(tmp)
            row_dict.append(file)

# print('arr:', arr)
# print('=======================')
X = np.array(arr)
# print('X:', X)
# print(np.unique(list(map(len, X))))
# number of clusters*****************
k = 8

# Machine Learning
kmeans = KMeans(n_clusters = k)
# important code:
kmeans.fit(X)
y_kmeans = kmeans.predict(X)
print(y_kmeans)

# centers = kmeans.cluster_centers_
# plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);

# in row_dict we store actual meanings of rows, in my case it's russian words
clusters = {}
n = 0
for item in y_kmeans:
    if item in clusters:
        clusters[item].append(row_dict[n])
    else:
        clusters[item] = [row_dict[n]]
    n +=1

# for item in clusters:
#     print("Cluster ", item)
#     for i in clusters[item]:
#         print(i)

for item in sorted(clusters):
    print("Cluster ", item)
    print(clusters[item])

# Plot points by clusters
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# color: red is the beginning
time = list(range(300, 0, -1))

# Reorganize the printings
for item in sorted(clusters):
    print("Cluster ", item)

    # create the plot windows
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in clusters[item]:
        data = pd.read_csv(os.path.join(SUBDIRECT, i))
        X = data['posX'].values[::100]
        Y = data['posZ'].values[::100]

        t_size = len(X)
        # colorGrad customized
        colorGrad = []
        for i in range(0, t_size):
            colorGrad.append([i/t_size, 0, 1 - i/t_size])

        time = list(range(0, t_size))

        ax.scatter(X, Y, time, c=colorGrad)
        # plt.scatter(X, Y, time, c=c, marker=m)
    plt.show()
