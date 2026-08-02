# flowtracks_examples

## Getting Started (Local Setup)

Clone the repository:
```bash
git clone https://github.com/openptv/flowtracks_examples.git
cd flowtracks_examples
```

Install *uv* (if not already installed):

Install dependencies and sync environment using uv:
```bash
uv sync
```

If you are developing alongside the `postptv` library, you can point the
dependency to a local checkout instead of the published package:

```bash
# In pyproject.toml, add (or uncomment):
#
# [tool.uv.sources]
# flowtracks = { path = "../postptv", editable = true }
#
# Then re-lock:
uv lock
uv sync
```

## Running the Examples & Gallery Index

To open the interactive **Marimo Gallery & Library Index** (`index.py`):

```bash
uv run marimo edit index.py
# or
uv run marimo edit gallery.py
```

The gallery index provides a searchable card interface with category filters (`Data Loading & Zarr`, `Visualization`, `Analysis & Scene Studies`), tag filtering, and instant notebook launch buttons.

Individual notebooks can also be opened directly:

```bash
# Open a single notebook
uv run marimo edit notebooks/marimo_aorta_flowtracks.py
```

## Test Data

Test data is available in the `test_zarr` folder (pre-built Zarr trajectory stores),
the `test_data` folder (`ptv_is`, `xuap`, `xuag`, and `trajPoint` text files for frames
101000–101025), and the `test_h5` folder (pre-built HDF5 Scene files). Some examples
also use files in `test_mat/`.

`flowtracks` now natively supports reading and writing cloud-native **Zarr stores**
via `flowtracks.io.read_zarr_trajectories()` and `flowtracks.io.save_zarr_trajectories()`,
as well as auto-detecting `.zarr` paths in `flowtracks.io.trajectories()`.


## Flowtracks Example Notebooks Catalog

Welcome to the Flowtracks example notebooks! All Jupyter notebook examples and scripts have been converted to reactive **marimo** notebooks.

### Data Loading & Zarr
- **[flowtracks_load_data_to_hdf_and_plot3d.py](notebooks/flowtracks_load_data_to_hdf_and_plot3d.py)**: Load data into Zarr/HDF format and create 3D trajectory plots.
- **[marimo_aorta_flowtracks.py](notebooks/marimo_aorta_flowtracks.py)**: End-to-end 3D cardiac aortic flow processing driving smoothing and Eulerian binning from `run.zarr`.
- **[plotting_trajectories_using_postptv.py](notebooks/plotting_trajectories_using_postptv.py)**: Auto-detect Zarr stores, HDF5, or `ptv_is` text files.
- **[plotting_2d_trajectories_using_openptv_postptv.py](notebooks/plotting_2d_trajectories_using_openptv_postptv.py)**: 2D XY projection of trajectories.
- **[postptv_EX3915.py](notebooks/postptv_EX3915.py)**: Ingest PTVis trajectory files, compute velocity/acceleration arrays, and plot PDFs.
- **[read_alex_ruiz_data.py](notebooks/read_alex_ruiz_data.py)**: Read v7.3 MAT files using `hdf5storage` and export Trajectory lists to Zarr.
- **[read_alex_ruiz_data-h5py.py](notebooks/read_alex_ruiz_data-h5py.py)**: Read MATLAB datasets directly with `h5py` and convert to PyTables HDF5 & Zarr stores.

### Visualization (2D / 3D / Plotly)
- **[marimo_zarr_dashboard.py](notebooks/marimo_zarr_dashboard.py)**: Interactive Zarr data dashboard inspecting chunked trajectory stores and velocity fields.
- **[plotly_visualize_trajectories_nb.py](notebooks/plotly_visualize_trajectories_nb.py)**: Interactive 3D Plotly trajectory visualizer with time window sliders and speed colormaps.
- **[plotly_3d_trajectories.py](notebooks/plotly_3d_trajectories.py)**: 3D line plot of particle trajectories grouped by ID using Plotly Express.
- **[myptv_visualization.py](notebooks/myptv_visualization.py)**: Render 3D trajectories with speed-dependent viridis colormapping.
- **[plot_frames.py](notebooks/plot_frames.py)**: Plot multi-panel 2D (x-y, y-z) and 3D frame snapshots.
- **[animate_trajectories.py](notebooks/animate_trajectories.py)**: Generate high-resolution MP4 video animations of particle tails with camera controls.

### Analysis & Scene Studies
- **[pair_analysis_example.py](notebooks/pair_analysis_example.py)**: Pairwise particle trajectory analysis with velocity magnitude 3D scatter plots.
- **[joint_pdf.py](notebooks/joint_pdf.py)**: Compute joint probability density functions (PDF) of velocity vs acceleration.
- **[test_plot_pdf_subplots.py](notebooks/test_plot_pdf_subplots.py)**: Fit Gaussian distributions to particle velocity components and plot subplots.
- **[hdf5_scene_analysis.py](notebooks/hdf5_scene_analysis.py)**: Explore tracer and particle scenes iterating by frame, segment, and trajectory.
- **[linking_trajectories.py](notebooks/linking_trajectories.py)**: Bridge broken trajectory gaps using predictive kinematic velocity matching.
- **[repeated_interpolation.py](notebooks/repeated_interpolation.py)**: Evaluate local velocity interpolation consistency via random subsampling.


---

## Why Flowtracks?
Flowtracks provides a robust, extensible platform for working with particle tracking data. These notebooks showcase how you can:
- Load data from a variety of sources
- Visualize trajectories in 2D and 3D
- Perform advanced statistical and pairwise analyses

Explore the notebooks above to see Flowtracks in action and accelerate your research or application development!

![](3dtraj.png)

