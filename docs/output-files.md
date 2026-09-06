# Output files

## Dictionary files (`dict`)

Written to the directory you run `dict` in. `X` in a filename is the sub-lattice number.

| File | Contents |
| --- | --- |
| `.cellpos` | Coordinates of every atom in the reduced unit cell |
| `initsub`, `finsub` | Atoms present in each sub-lattice (before / after equivalencing) |
| `.basisX` | Coordinates of the numbered nearest-neighbour positions for sub-lattice `X`. The `Atom No.` column is the neighbour label used to reconstruct configurations |
| `.symX` | Nearest-neighbour atoms `1…N` and their symmetry-rotated forms — feeds the binary labelling system |
| `.cfgdictX` | Every possible configuration in the system (decimal notation) and its Configuration label |
| `.binomX` | Ordered Configuration labels, the multiplicity of each for the lattice, and its number of "dislike" atoms |

## Analysis files (`config`)

Written next to each input `.rmc6f`. `STEMNAME` is the input file's name.

### Histograms

`STEMNAME_XC_subY_EF.png` and its `_A` / `_B` / `_AB` variants.

- `_XC` — the pseudo-binary this histogram is built from (`X` = constituent-atom number
  as listed under `ATOMS` in the `.rmc6f`).
- `_subY` — the sub-lattice.
- `_A` / `_B` — centred on one side of the pseudo-binary; `_AB` — both, overlaid with a
  legend; **no suffix** — the total histogram of enhanced configurations.

The y-axis is the enhancement factor **β**; the x-axis is the Clapp configuration label
(`CC`).

### `.clapp` and `_EF.clapp`

| File | Contents |
| --- | --- |
| `STEMNAME_subY.clapp` | Every atom in the large box — coordinates, type, and its configuration in each pseudo-binary — plus the box dimensions |
| `STEMNAME_subY_EF.clapp` | **The analysis result.** For each Clapp configuration: the atom count and statistical enhancement, broken down by pseudo-binary and by atom A / B / total. The final `total` column is the overall enhancement of that configuration in the system |

### `_mb.rmc6f`

A second `.rmc6f` with every atom moved to its ideal lattice site (displacements
averaged out). Skipped automatically when it would otherwise be picked up by
`--rmc6f-glob`.
