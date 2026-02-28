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
uv pip install --upgrade pip
uv sync
```

## Running the Examples

To run it without installations:

```bash
uvx marimo run gallery.py
```


## Test Data

Test data is available in the `test_data` folder.
## Example Notebooks and Online Viewing

Flowtracks documentation: https://flowtracks.readthedocs.io/en/latest/

### View Notebooks Online

You can view the example notebooks directly on molab.marimo.io:

1. Go to https://molab.marimo.io
2. Click "Open from GitHub"
3. Enter the repository URL: `https://github.com/openptv/flowtracks_examples`
4. Browse and open any notebook from the `jupyter_notebooks` folder

## Flowtracks Example Notebooks

Welcome to the Flowtracks example notebooks! These interactive marimo notebooks demonstrate the core features and strengths of Flowtracks, including flexible data loading, powerful visualization, and advanced analysis tools for particle tracking data.

## Table of Contents
- [Getting Started](#getting-started)
- [Data Loading](#data-loading)
- [Visualization](#visualization)
- [Analysis](#analysis)

## Getting Started
- **[postptv_EX3915.py](postptv_EX3915.py)**: Load and visualize trajectories from PTVis data.
- **[flowtracks_load_data_to_hdf_and_plot3d.py](flowtracks_load_data_to_hdf_and_plot3d.py)**: Load data into HDF format and create 3D trajectory plots.

## Data Loading
- **[read_alex_ruiz_data.py](read_alex_ruiz_data.py)**: Load and process data from the Alex Ruiz dataset.
- **[read_alex_ruiz_data-h5py.py](read_alex_ruiz_data-h5py.py)**: Alternative data loading using h5py.
- **[plotting_trajectories_using_postptv.py](plotting_trajectories_using_postptv.py)**: Load and plot trajectories using postptv.

## Visualization
- **[plotly_visualize_trajectories_nb.py](plotly_visualize_trajectories_nb.py)**: Interactive 2D/3D trajectory visualization with Plotly.
- **[plotly_3d_trajectories.py](plotly_3d_trajectories.py)**: 3D trajectory visualization using Plotly.
- **[myptv_visualization.py](myptv_visualization.py)**: Visualize trajectories with myPTV tools.
- **[plotting_2d_trajectories_using_openptv_postptv.py](plotting_2d_trajectories_using_openptv_postptv.py)**: 2D trajectory visualization using OpenPTV/PostPTV.
- **[plot_frames.py](plot_frames.py)**: Visualize individual frames of trajectory data.
- **[animate_trajectories.py](animate_trajectories.py)**: Create animations of particle trajectories.

## Analysis
- **[pair_analysis_example.py](pair_analysis_example.py)**: Example of pairwise trajectory analysis.
- **[joint_pdf.py](joint_pdf.py)**: Statistical analysis and joint PDF plotting.
- **[test_plot_pdf_subplots.py](test_plot_pdf_subplots.py)**: Test and visualize PDF subplots for trajectory data.

---

## Why Flowtracks?
Flowtracks provides a robust, extensible platform for working with particle tracking data. These notebooks showcase how you can:
- Load data from a variety of sources
- Visualize trajectories in 2D and 3D
- Perform advanced statistical and pairwise analyses

Explore the notebooks above to see Flowtracks in action and accelerate your research or application development!

![](3dtraj.png)

