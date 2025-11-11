
import argparse, csv
from pathlib import Path
import numpy as np
import trimesh
from .utils import load_mesh, save_mesh, stats, ensure_dir, save_json
from . import normalize as norm
from . import quantize as qtz
from .metrics import mse, mae, chamfer, hausdorff
from .visualize import plot_error_axes, side_by_side_render
from .seam_tokenizer import detect_seams, tokens_from_seams, save_seam_visualization

def process_mesh(mesh_path: str, out_dir: str, bins: int = 1024, k_density: int = 16, alpha: float = 1.0):
    name = Path(mesh_path).stem
    od = Path(out_dir)/name
    ensure_dir(od)

    mesh = load_mesh(mesh_path)
    V = mesh.vertices.copy()
    F = mesh.faces.copy()

    s = stats(V)
    save_json(s, str(od/'stats.json'))

    rows = []
    for method in ('minmax', 'unit_sphere'):
        if method=='minmax':
            Vn, ctx = norm.minmax_normalize(V)
            denorm = norm.minmax_denormalize
        else:
            Vn, ctx = norm.unit_sphere_normalize(V)
            denorm = norm.unit_sphere_denormalize

        q = qtz.uniform_quantize(Vn, bins)
        Vn_rec = qtz.uniform_dequantize(q, bins)
        V_rec = denorm(Vn_rec, ctx)
        recons = trimesh.Trimesh(V_rec, F, process=False)
        side_by_side_render(mesh.copy(), recons.copy(), str(od/f"{method}_compare.png"))
        save_mesh(V_rec, F, str(od/f"{method}_recon.obj"))
        msev = mse(V, V_rec); maev = mae(V,V_rec)
        ch = chamfer(V,V_rec); hd = hausdorff(V,V_rec)
        plot_error_axes(msev, maev, str(od/f"{method}_errors.png"))
        rows.append([name, method, 'uniform', bins, float(msev.mean()), float(maev.mean()), ch, hd])

        bins_per_vertex, density_norm = qtz.adaptive_bins_per_vertex(Vn, k=k_density, base_bins=bins, alpha=alpha)
        qA = qtz.adaptive_quantize(Vn, bins_per_vertex)
        VnA = qtz.adaptive_dequantize(qA, bins_per_vertex)
        V_recA = denorm(VnA, ctx)
        reconsA = trimesh.Trimesh(V_recA, F, process=False)
        save_mesh(V_recA, F, str(od/f"{method}_adaptive_recon.obj"))
        side_by_side_render(mesh.copy(), reconsA.copy(), str(od/f"{method}_adaptive_compare.png"))
        msevA = mse(V, V_recA); maevA = mae(V,V_recA)
        chA = chamfer(V,V_recA); hdA = hausdorff(V,V_recA)
        plot_error_axes(msevA, maevA, str(od/f"{method}_adaptive_errors.png"))
        import numpy as np
        np.save(str(od/'bins_per_vertex.npy'), bins_per_vertex)
        rows.append([name, method, 'adaptive', int(bins), float(msevA.mean()), float(maevA.mean()), chA, hdA])

    seams = detect_seams(mesh)
    tokens = tokens_from_seams(mesh, seams)
    save_json(tokens, str(od/'seams_tokens.json'))
    save_seam_visualization(mesh, seams, str(od/'seams_visualization.ply'))

    with open(od/'summary.csv','w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['mesh','norm_method','quant','bins','mse_mean','mae_mean','chamfer','hausdorff'])
        w.writerows(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input_dir', default='meshes')
    ap.add_argument('--out_dir', default='results')
    ap.add_argument('--bins', type=int, default=1024)
    ap.add_argument('--k_density', type=int, default=16)
    ap.add_argument('--alpha', type=float, default=1.0)
    args = ap.parse_args()

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    for p in Path(args.input_dir).glob('*.obj'):
        process_mesh(str(p), args.out_dir, bins=args.bins, k_density=args.k_density, alpha=args.alpha)

if __name__=='__main__':
    main()
