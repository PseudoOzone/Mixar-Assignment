# Mixar Assignment — Mesh Processing and Procedural Editing

A CPU-based 3D mesh assignment implementing normalization, uniform and adaptive quantization, reconstruction-error analysis, seam tokenization, prompt-driven geometric transforms, heightmap-based image-to-mesh conversion, and procedural text-to-texture generation.

**Author:** Anshuman Bakshi  
**Context:** Final-year B.Tech software-engineering assignment

> **Status:** technical assignment and baseline implementation. The “prompt,” image-to-3D, and text-to-texture features are deterministic utilities rather than generative foundation-model pipelines.

## Implemented components

### Mesh processing

- Min-max normalization and denormalization
- Unit-sphere normalization and denormalization
- Uniform vertex quantization
- Density-adaptive quantization
- OBJ reconstruction
- MSE and MAE by coordinate axis
- Chamfer and Hausdorff distance
- Side-by-side renders and CSV summaries

### Seam analysis

- Seam detection
- Seam-token generation
- PLY seam visualization

### Prompt editor

Parses a limited command grammar for transforms such as scale, rotation, and translation. It does not call an LLM.

### Image to mesh

Builds a baseline height-field mesh from an input image. It does not infer complete 3D geometry from a single photograph.

### Text to texture

Creates procedural texture patterns from supported text keywords and updates an OBJ/MTL reference. It is not a diffusion-based texture generator.

## Setup

Python 3.10 or 3.11 is recommended.

```bash
git clone https://github.com/PseudoOzone/Mixar-Assignment.git
cd Mixar-Assignment

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS or Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the mesh pipeline

```bash
python -m src.pipeline --input_dir meshes --out_dir results --bins 1024
```

Every direct `.obj` file in `meshes/` is processed. Per-mesh results are written below `results/<mesh-name>/`.

Typical artifacts include:

```text
stats.json
summary.csv
minmax_recon.obj
minmax_compare.png
minmax_errors.png
unit_sphere_recon.obj
unit_sphere_compare.png
unit_sphere_errors.png
seams_tokens.json
seams_visualization.ply
```

## Prompt editor

```bash
python -m src.prompt_editor \
  --mesh meshes/cube.obj \
  --out meshes/cube_edited.obj \
  --prompt "scale by 1.3, rotate 30 deg around z, translate x by 0.2"
```

Only transformations supported by the parser are applied.

## Image to mesh

```bash
python -m src.image_to_3d \
  --image assets/sample_height.png \
  --out meshes/heightmesh.obj \
  --size 128 \
  --height 0.2
```

The output is a heightmap reconstruction, not an object-complete image-to-3D model.

## Text to texture

```bash
python -m src.text_to_texture \
  --mesh meshes/sphere.obj \
  --prompt "checkerboard blue white"
```

The command creates a procedural PNG and updates the mesh material reference.

## Known limitations

- A malformed or unsupported OBJ can stop the entire batch because per-mesh exceptions are not isolated.
- Empty and degenerate meshes are not validated before normalization and metrics.
- Command-line arguments such as `bins`, `k_density`, and `alpha` need stronger range checks.
- Only OBJ files directly inside the input directory are discovered.
- Rendering may fall back to 2D projections when an OpenGL context is unavailable.
- The pipeline imports NumPy twice and can be simplified.
- Chamfer and Hausdorff calculations can become expensive on high-resolution meshes.
- Output folders can be overwritten without a run identifier or manifest.
- There is no automated test suite or CI workflow.

## Recommended improvements

- add mesh validation and actionable errors
- continue processing after a single-file failure
- write a run-level manifest with versions and parameters
- add deterministic tests for normalization and quantization round trips
- support recursive file discovery and additional mesh formats
- benchmark adaptive quantization against uniform quantization across varied topology
- separate CLI orchestration from reusable processing functions

## License

Educational and assignment use only unless a separate license file states otherwise.
