# Mixar Assignment — Mesh Pipeline + Prompt Editor + Img2Mesh + Text2Texture

**Author:** Anshuman Bakshi  
**Email:** bakshianshuman117@gmail.com  
**Program:** Final Year B.Tech CSE — SWE

This repo implements the **3D mesh processing pipeline** (normalization, quantization, error analysis), plus:
- **Prompt-based editor** interface to edit meshes with natural language (no API key required).
- **Image → 3D** baseline via heightmap reconstruction.
- **Text → Texture** procedural material generation.

The layout follows the structure of the reference repo.

## Install
```bash
pip install -r requirements.txt
```

## Run (Core Pipeline)
```bash
python -m src.pipeline --input_dir meshes --out_dir results --bins 1024
```
This will run **Min–Max** and **Unit-Sphere** normalization, quantize/dequantize, reconstruct, compute errors (MSE/MAE/Chamfer), save comparison renders and CSV summaries.

## Run (Prompt Editor)
```bash
python -m src.prompt_editor --mesh meshes/cube.obj --out meshes/cube_edited.obj --prompt "scale by 1.3, rotate 30 deg around z, translate x by 0.2"
```

## Run (Image → 3D)
```bash
python -m src.image_to_3d --image assets/sample_height.png --out meshes/heightmesh.obj --size 128 --height 0.2
```

## Run (Text → Texture)
```bash
python -m src.text_to_texture --mesh meshes/sphere.obj --prompt "checkerboard blue white"
```
This saves a PNG texture and updates the OBJ's MTL to reference it.

## Results
See the `results/` folder for per-mesh outputs (plots, CSV, reconstructed OBJs). This archive already includes generated results for the included **cube** and **sphere** test meshes.

## Notes
- If OpenGL context is unavailable, rendering falls back to 2D projections.
- Everything runs on CPU.