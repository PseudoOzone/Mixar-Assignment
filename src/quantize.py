
import numpy as np

def uniform_quantize(Vn: np.ndarray, bins: int):
    q = np.clip(np.floor(Vn * (bins - 1)), 0, bins - 1).astype(np.int32)
    return q

def uniform_dequantize(q: np.ndarray, bins: int):
    return q.astype(np.float32) / float(bins - 1)

def adaptive_bins_per_vertex(Vn: np.ndarray, k: int = 16, base_bins: int = 1024, alpha: float = 1.0):
    from sklearn.neighbors import NearestNeighbors
    n_neighbors = min(k, max(2, len(Vn)-1))
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(Vn)
    dists, _ = nbrs.kneighbors(Vn)
    if dists.shape[1] > 1:
        md = dists[:,1:].mean(axis=1)
    else:
        md = dists.mean(axis=1)
    density = 1.0 / (md + 1e-8)
    dn = (density - density.min()) / (density.max() - density.min() + 1e-12)
    bins = np.clip((base_bins * (1.0 + alpha * dn)).astype(int), base_bins, base_bins*4)
    return bins, dn

def adaptive_quantize(Vn: np.ndarray, bins_per_vertex: np.ndarray):
    q = np.zeros_like(Vn, dtype=np.int32)
    for i in range(Vn.shape[0]):
        b = int(bins_per_vertex[i])
        q[i] = np.clip(np.floor(Vn[i] * (b - 1)), 0, b - 1).astype(np.int32)
    return q

def adaptive_dequantize(q: np.ndarray, bins_per_vertex: np.ndarray):
    Vn = np.zeros_like(q, dtype=np.float32)
    for i in range(q.shape[0]):
        b = float(bins_per_vertex[i])
        Vn[i] = q[i].astype(np.float32) / max(b - 1.0, 1.0)
    return Vn
