# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.20.2",
# ]
# ///
import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this notebook we go through the process of reading trajectories and displaying their XY projection, as an example of how to manipulate trajectory objects. Naturally, trajectories contain 3D data, but here we only use a 2D view for simplicity.

    The first step is to import the necessary modules. We use Matplotlib's pyplot for simple plotting commands, and ``flowtracks.io`` is the module supplied by the PostPTV project for reading trajectories in various formats, including the new cloud-native **Zarr** format (`.zarr`), HDF5 (`.h5`), and legacy text files (`ptv_is.%d`).
    """)
    return


@app.cell
def _():
    from matplotlib import pyplot
    from flowtracks.io import trajectories, read_zarr_trajectories

    return pyplot, read_zarr_trajectories, trajectories


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the next step we load our trajectories using `flowtracks.io.trajectories()`, which automatically detects whether the target path is a cloud-native **Zarr store**, an HDF5 file, or a `ptv_is.%d` text template.

    Note that we request only trajectories at least 3 frames long to be read. For large data sets, this saves a lot of memory in the reading process.
    """)
    return


@app.cell
def _(trajectories):
    from pathlib import Path
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    zarr_dir = base_dir / 'test_zarr' / 'trajectories.zarr' if (base_dir / 'test_zarr').exists() else base_dir / '..' / 'test_zarr' / 'trajectories.zarr'
    data_dir = base_dir if (base_dir / 'test_data').exists() else base_dir / '..' / 'test_data'

    if zarr_dir.exists():
        inName = str(zarr_dir)
        trajects = trajectories(inName, traj_min_len=3)
    else:
        inName = str(data_dir / 'ptv_is.%d')
        trajects = trajectories(inName, traj_min_len=3)
    return (trajects,)



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, we create a figure and plot the trajectories. For each trajectory, the ``.pos()`` method returns a $(t,3)$-shaped array for $t$ frames where the trajectory is present. Other methods available include ``velocity()`` and ``accel()``.
    """)
    return


@app.cell
def _(pyplot, trajects):
    pyplot.figure(figsize=(12, 10))
    for _traj in trajects:
        pyplot.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], '.')
    pyplot.show()
    return


@app.cell
def _(trajects):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for _traj in trajects:
        ax.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], _traj.pos()[:, 2], '.')
    plt.show()
    return


if __name__ == "__main__":
    app.run()
