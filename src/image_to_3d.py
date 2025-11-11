
import argparse
import numpy as np
from PIL import Image
from .utils import save_mesh

def heightmap_to_mesh(img: Image.Image, size: int = 128, height: float = 0.2):
    img = img.convert('L').resize((size,size))
    H = np.asarray(img, dtype=np.float32)/255.0
    xs = np.linspace(-0.5,0.5,size)
    ys = np.linspace(-0.5,0.5,size)
    xv,yv = np.meshgrid(xs, ys)
    V = np.stack([xv, yv, H*height], axis=-1).reshape(-1,3)
    faces = []
    for y in range(size-1):
        for x in range(size-1):
            i = y*size + x
            faces.append([i, i+1, i+size])
            faces.append([i+1, i+size+1, i+size])
    F = np.array(faces, dtype=np.int32)
    return V,F

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--size', type=int, default=128)
    ap.add_argument('--height', type=float, default=0.2)
    args = ap.parse_args()

    img = Image.open(args.image)
    V,F = heightmap_to_mesh(img, args.size, args.height)
    save_mesh(V,F,args.out)

if __name__=='__main__':
    main()
