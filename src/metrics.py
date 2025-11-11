
import numpy as np
from scipy.spatial import cKDTree

def mse(a,b):
    return ((a-b)**2).mean(axis=0)

def mae(a,b):
    return np.abs(a-b).mean(axis=0)

def chamfer(a,b):
    ta = cKDTree(a); tb = cKDTree(b)
    da, _ = ta.query(b, k=1)
    db, _ = tb.query(a, k=1)
    return float(da.mean() + db.mean())

def hausdorff(a,b):
    ta = cKDTree(a); tb = cKDTree(b)
    da, _ = ta.query(b, k=1)
    db, _ = tb.query(a, k=1)
    return float(max(da.max(), db.max()))
