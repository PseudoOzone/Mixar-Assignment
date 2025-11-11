
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import trimesh

def plot_error_axes(mse_vec, mae_vec, out_path):
    axes = ['x','y','z']
    x = np.arange(3)
    plt.figure()
    plt.bar(x-0.15, mse_vec, width=0.3, label='MSE')
    plt.bar(x+0.15, mae_vec, width=0.3, label='MAE')
    plt.xticks(x, axes)
    plt.ylabel('Error')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def side_by_side_render(orig: trimesh.Trimesh, recon: trimesh.Trimesh, out_path: str):
    try:
        s = trimesh.Scene()
        orig.visual.vertex_colors = [200,50,50,255]
        recon.visual.vertex_colors = [50,200,50,255]
        s.add_geometry([orig, recon])
        png = s.save_image(resolution=(800,400))
        if png is not None:
            Path(out_path).write_bytes(png)
            return
    except Exception:
        pass
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,4))
    plt.subplot(1,2,1)
    ov = orig.vertices
    plt.scatter(ov[:,0], ov[:,1], s=1)
    plt.title('Original (XY)')
    plt.axis('equal')
    plt.subplot(1,2,2)
    rv = recon.vertices
    plt.scatter(rv[:,0], rv[:,1], s=1)
    plt.title('Reconstructed (XY)')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
