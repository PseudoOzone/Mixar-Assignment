
import numpy as np
import json
from pathlib import Path
import trimesh
from collections import defaultdict

def _boundary_edges_from_faces(faces: np.ndarray):
    counts = defaultdict(int)
    for f in faces:
        e01 = tuple(sorted((int(f[0]), int(f[1]))))
        e12 = tuple(sorted((int(f[1]), int(f[2]))))
        e20 = tuple(sorted((int(f[2]), int(f[0]))))
        counts[e01]+=1; counts[e12]+=1; counts[e20]+=1
    boundary = [e for e,c in counts.items() if c==1]
    if len(boundary)==0:
        return np.empty((0,2), dtype=int)
    return np.array(boundary, dtype=int)

def detect_seams(mesh: trimesh.Trimesh, dihedral_deg: float = 30.0):
    boundary_edges = _boundary_edges_from_faces(mesh.faces)

    sharp_edges = np.empty((0,2), dtype=int)
    try:
        if len(mesh.face_adjacency_angles) > 0:
            sharp_idx = mesh.face_adjacency_angles > np.deg2rad(dihedral_deg)
            sharp_edges = mesh.face_adjacency_edges[sharp_idx]
    except Exception:
        pass

    try:
        vn = mesh.vertex_normals
        var = np.var(vn, axis=1)
        high_var_vertices = np.where(var > np.percentile(var, 90))[0]
    except Exception:
        high_var_vertices = np.array([], dtype=int)

    return {
        'boundary_edges': boundary_edges,
        'sharp_edges': sharp_edges,
        'high_var_vertices': high_var_vertices
    }

def tokens_from_seams(mesh: trimesh.Trimesh, seams: dict):
    tokens = []
    for e in seams['boundary_edges'][:10000]:
        v0, v1 = int(e[0]), int(e[1])
        length = float(np.linalg.norm(mesh.vertices[v0]-mesh.vertices[v1]))
        tokens.append({'t':'E','v0':v0,'v1':v1,'l':length})
    for e in seams['sharp_edges'][:10000]:
        v0, v1 = int(e[0]), int(e[1])
        length = float(np.linalg.norm(mesh.vertices[v0]-mesh.vertices[v1]))
        tokens.append({'t':'S','v0':v0,'v1':v1,'l':length})
    for v in seams['high_var_vertices'][:10000]:
        tokens.append({'t':'V','v':int(v)})
    return tokens

def save_seam_visualization(mesh: trimesh.Trimesh, seams: dict, out_path: str):
    mesh = mesh.copy()
    colors = np.tile(np.array([200,200,200,255], dtype=np.uint8), (len(mesh.vertices),1))
    for e in seams['boundary_edges']:
        colors[e[0]] = [255,50,50,255]; colors[e[1]] = [255,50,50,255]
    for e in seams['sharp_edges']:
        colors[e[0]] = [50,50,255,255]; colors[e[1]] = [50,50,255,255]
    mesh.visual.vertex_colors = colors
    mesh.export(out_path)

def run(mesh_path: str, out_dir: str):
    m = trimesh.load(mesh_path, force='mesh')
    seams = detect_seams(m)
    tokens = tokens_from_seams(m, seams)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    json_path = str(Path(out_dir)/'seams_tokens.json')
    with open(json_path,'w') as f:
        json.dump(tokens, f, indent=2)
    save_seam_visualization(m, seams, str(Path(out_dir)/'seams_visualization.ply'))
    return json_path
