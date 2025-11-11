
import os
import json
from pathlib import Path
import numpy as np
import trimesh

def load_mesh(path):
    mesh = trimesh.load(path, force='mesh')
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = trimesh.util.concatenate(mesh.dump())
    return mesh

def save_mesh(vertices, faces, out_path):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.export(out_path)
    return out_path

def stats(vertices: np.ndarray):
    return {
        'num_vertices': int(vertices.shape[0]),
        'min': vertices.min(axis=0).tolist(),
        'max': vertices.max(axis=0).tolist(),
        'mean': vertices.mean(axis=0).tolist(),
        'std': vertices.std(axis=0).tolist(),
    }

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def save_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)

def write_mtl_and_link(obj_path: str, texture_path: str, mtl_name='mat1'):
    obj_path = Path(obj_path)
    texture_rel = os.path.relpath(texture_path, obj_path.parent)
    mtl_path = obj_path.with_suffix('.mtl')
    mtl_content = f"""newmtl {mtl_name}
Ka 1.000 1.000 1.000
Kd 1.000 1.000 1.000
Ks 0.000 0.000 0.000
d 1.0
illum 1
map_Kd {texture_rel}
"""
    with open(mtl_path, 'w') as f:
        f.write(mtl_content)
    lines = obj_path.read_text().splitlines()
    has_mtllib = any(l.strip().startswith('mtllib') for l in lines[:5])
    if not has_mtllib:
        lines.insert(0, f"mtllib {mtl_path.name}")
        lines.insert(1, f"usemtl {mtl_name}")
        obj_path.write_text("\n".join(lines))
    return str(mtl_path)
