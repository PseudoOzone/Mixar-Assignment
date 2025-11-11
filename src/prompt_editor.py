
import argparse
import numpy as np
from .utils import load_mesh, save_mesh

def parse_prompt(prompt: str):
    ops = []
    words = prompt.lower().replace(',', ' ').split()
    i=0
    while i < len(words):
        w = words[i]
        if w.startswith('scale'):
            s = 1.0
            if i+2 < len(words) and words[i+1]=='by':
                try: s = float(words[i+2]); i+=2
                except: pass
            ops.append(('scale', s))
        elif w.startswith('rotate'):
            angle = 0.0; axis='z'
            if i+1 < len(words):
                try: angle = float(words[i+1]); i+=1
                except: pass
            if i+1 < len(words) and words[i+1] in ('deg','degree','degrees'):
                i+=1
            if i+2 < len(words) and words[i+1]=='around':
                axis = words[i+2]; i+=2
            ops.append(('rotate', axis, np.deg2rad(angle)))
        elif w in ('translate','move','shift'):
            axis=None; val=0.0
            if i+1 < len(words): axis = words[i+1]; i+=1
            if i+1 < len(words) and words[i+1]=='by':
                try: val = float(words[i+2]); i+=2
                except: pass
            ops.append(('translate', axis, val))
        i+=1
    return ops

def apply_ops(V: np.ndarray, ops):
    V = V.copy()
    for op in ops:
        if op[0]=='scale':
            s = op[1]
            V *= s
        elif op[0]=='rotate':
            axis, ang = op[1], op[2]
            c,s = np.cos(ang), np.sin(ang)
            if axis.startswith('x'):
                R = np.array([[1,0,0],[0,c,-s],[0,s,c]])
            elif axis.startswith('y'):
                R = np.array([[c,0,s],[0,1,0],[-s,0,c]])
            else:
                R = np.array([[c,-s,0],[s,c,0],[0,0,1]])
            V = V @ R.T
        elif op[0]=='translate':
            axis, val = op[1], op[2]
            d = np.zeros(3)
            idx = {'x':0,'y':1,'z':2}.get(axis[0],2)
            d[idx]=val
            V += d
    return V

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mesh', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--prompt', required=True)
    args = ap.parse_args()

    m = load_mesh(args.mesh)
    V = m.vertices.copy()
    ops = parse_prompt(args.prompt)
    V2 = apply_ops(V, ops)
    save_mesh(V2, m.faces, args.out)

if __name__=='__main__':
    main()
