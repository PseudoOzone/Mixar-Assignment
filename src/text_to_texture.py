
import argparse, re
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from .utils import write_mtl_and_link

def color_from_words(prompt: str):
    colors = {
        'red': (220,60,60), 'green': (60,220,60), 'blue': (60,120,240),
        'white': (240,240,240), 'black': (20,20,20), 'yellow': (240,220,60),
        'purple': (150,60,200), 'orange': (255,140,60), 'gray': (160,160,160)
    }
    found = [colors[w] for w in colors if re.search(r'\b'+re.escape(w)+r'\b', prompt.lower())]
    if not found:
        return (200,200,200), (50,50,50)
    if len(found)==1:
        return found[0], (20,20,20)
    return found[0], found[1]

def generate_texture(prompt: str, size=512):
    base, accent = color_from_words(prompt)
    img = Image.new('RGB', (size,size), base)
    draw = ImageDraw.Draw(img)
    low = prompt.lower()
    if 'checker' in low or 'checkerboard' in low:
        step = size//8
        for y in range(0,size,step):
            for x in range(0,size,step):
                if ((x//step)+(y//step))%2==0:
                    draw.rectangle([x,y,x+step-1,y+step-1], fill=accent)
    elif 'stripes' in low:
        step = size//12
        for x in range(0,size,step*2):
            draw.rectangle([x,0,x+step-1,size-1], fill=accent)
    else:
        step = size//16
        for y in range(step//2,size,step):
            for x in range(step//2,size,step):
                draw.ellipse([x-4,y-4,x+4,y+4], fill=accent)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mesh', required=True)
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--out_texture', default=None)
    args = ap.parse_args()

    mpath = Path(args.mesh)
    tex = generate_texture(args.prompt)
    out_tex = args.out_texture or str(mpath.with_suffix('')) + '_texture.png'
    tex.save(out_tex)
    write_mtl_and_link(str(mpath), out_tex)

if __name__=='__main__':
    main()
