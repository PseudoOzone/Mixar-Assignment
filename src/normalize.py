
import numpy as np

def minmax_normalize(V: np.ndarray):
    vmin = V.min(axis=0)
    vmax = V.max(axis=0)
    scale = np.maximum(vmax - vmin, 1e-12)
    Vn = (V - vmin) / scale
    ctx = {'type':'minmax', 'vmin': vmin, 'vmax': vmax}
    return Vn, ctx

def minmax_denormalize(Vn: np.ndarray, ctx):
    vmin, vmax = ctx['vmin'], ctx['vmax']
    scale = np.maximum(vmax - vmin, 1e-12)
    return Vn * scale + vmin

def unit_sphere_normalize(V: np.ndarray):
    centroid = V.mean(axis=0)
    Vc = V - centroid
    radius = np.linalg.norm(Vc, axis=1).max()
    radius = max(radius, 1e-12)
    Vn = Vc / radius * 0.5 + 0.5
    ctx = {'type':'unit_sphere', 'centroid': centroid, 'radius': radius}
    return Vn, ctx

def unit_sphere_denormalize(Vn: np.ndarray, ctx):
    centroid, radius = ctx['centroid'], ctx['radius']
    Vc = (Vn - 0.5) * 2.0 * radius
    return Vc + centroid
