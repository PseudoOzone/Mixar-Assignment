
import numpy as np
from sklearn.cluster import KMeans

def cluster_density(Vn: np.ndarray, clusters: int = 4, random_state: int = 0):
    km = KMeans(n_clusters=clusters, n_init='auto', random_state=random_state)
    labels = km.fit_predict(Vn)
    return labels, km.cluster_centers_
