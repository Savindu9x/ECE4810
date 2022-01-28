# Written by Savindu9x
# Last Modified on 20-09-2021
# Import Libraries
import time
import matplotlib.colors
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
# Exporting required dataset file
import_file_path = "dataset_2.xlsx"
read_file = pd.read_excel(import_file_path)
df = DataFrame(read_file, columns=['x', 'y'])
#Compute clustering with kmeans
#Assign three clusters to df dataset
k = 5
start = time.monotonic()
kmeans = KMeans(n_clusters=k)
kmeans.fit(df)
print()
centroids = kmeans.cluster_centers_
end = time.monotonic()
cpu_time = round(end-start,3)
print("Computation time: ",cpu_time,"s")
kk = round((kmeans.inertia_), 2)
ss = silhouette_score(df, kmeans.labels_)
#Compute clustering with KMedoids Clustering
start = time.monotonic()
kmedoids = KMedoids(n_clusters=k, method='pam', init='k-medoids++', random_state=0)
kmedoids.fit(df)
centroids = kmedoids.cluster_centers_
kk = round((kmedoids.inertia_), 2)
end = time.monotonic()
cpu_time = round(end-start,3)
ss = silhouette_score(df, kmeans.labels_)
########################################################
# Plotting the results
figure = plt.figure(figsize=(8,6))
cm = plt.cm.RdBu
cm_bright = matplotlib.colors.ListedColormap(['#FF0000', '#0000FF'])
ax = plt.subplot(1,1,1)
plt.scatter(df['x'], df['y'], c=kmedoids.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
#plt.grid(True, which='major')
plt.xlabel("time(s)")
plt.ylabel("total distance (cm)")
plt.title("KMedoids clustering for (k=5) for distance dataset")
plt.text(16,25, 'Computational time: %.3f s\nInertia: %.2f' % (cpu_time, kk), fontsize=11)
plt.show()
# Visualization for distortion against k number of clusters.
K_cluster = range(1,10)
distortion = []
for k in K_cluster:
 kmeans = KMeans(n_clusters=k)
 kmeans.fit(df)
 distortion.append(sum(np.min(cdist(df,kmeans.cluster_centers_,'euclidean'), axis=1))/df.shape[0])

plt.figure(figsize=(9,5))
plt.plot(K_cluster,distortion, 'bx-')
plt.xlabel('Number of K')
plt.ylabel('Within Sum of Squares distance')
plt.title('Elbow method for varying K number of clusters')
plt.show()



