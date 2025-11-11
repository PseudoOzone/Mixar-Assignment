# Final Report — Mesh Normalization, Quantization & Error Analysis

**Author:** Anshuman Bakshi  
**Email:** bakshianshuman117@gmail.com  
**Program:** Final Year B.Tech CSE — SWE

## Results Summary
| mesh        | norm_method   | quant    |   bins |    mse_mean |    mae_mean |     chamfer |   hausdorff |
|:------------|:--------------|:---------|-------:|------------:|------------:|------------:|------------:|
| cube        | minmax        | uniform  |   1024 | 0           | 0           | 0           |  0          |
| cube        | minmax        | adaptive |   1024 | 0           | 0           | 0           |  0          |
| cube        | unit_sphere   | uniform  |   1024 | 1.00043e-06 | 0.00084652  | 0.00330154  |  0.00238899 |
| cube        | unit_sphere   | adaptive |   1024 | 1.00043e-06 | 0.00084652  | 0.00330154  |  0.00238899 |
| sphere      | minmax        | uniform  |   1024 | 3.02807e-07 | 0.000487235 | 0.00184238  |  0.00145253 |
| sphere      | minmax        | adaptive |   1024 | 1.38197e-07 | 0.000316684 | 0.00121674  |  0.00145253 |
| sphere      | unit_sphere   | uniform  |   1024 | 3.04295e-07 | 0.000488758 | 0.00184711  |  0.00145253 |
| sphere      | unit_sphere   | adaptive |   1024 | 1.38924e-07 | 0.000317749 | 0.00122004  |  0.00145253 |
| heightmesh  | minmax        | uniform  |   1024 | 2.08136e-07 | 0.000336535 | 0.0014787   |  0.00137906 |
| heightmesh  | minmax        | adaptive |   1024 | 8.99084e-08 | 0.000223848 | 0.000962747 |  0.00126336 |
| heightmesh  | unit_sphere   | uniform  |   1024 | 6.22725e-07 | 0.000685394 | 0.00262202  |  0.0023072  |
| heightmesh  | unit_sphere   | adaptive |   1024 | 2.77135e-07 | 0.000445459 | 0.00171911  |  0.00219134 |
| cube_edited | minmax        | uniform  |   1024 | 2.26125e-07 | 0.000259809 | 0.00155886  |  0.00104564 |
| cube_edited | minmax        | adaptive |   1024 | 2.26125e-07 | 0.000259809 | 0.00155886  |  0.00104564 |
| cube_edited | unit_sphere   | uniform  |   1024 | 1.48346e-06 | 0.00101585  | 0.00402486  |  0.00287581 |
| cube_edited | unit_sphere   | adaptive |   1024 | 1.48346e-06 | 0.00101585  | 0.00402486  |  0.00287581 |