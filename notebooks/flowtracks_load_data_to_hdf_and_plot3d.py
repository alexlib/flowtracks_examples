# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.20.2",
# ]
# ///
import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo
    from flowtracks.io import (
        trajectories,
        read_zarr_trajectories,
        save_zarr_trajectories,
        save_particles_table,
        trajectories_table,
    )
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from pathlib import Path

    return (
        Path,
        mo,
        plt,
        read_zarr_trajectories,
        save_zarr_trajectories,
        save_particles_table,
        trajectories,
        trajectories_table,
    )


@app.cell
def _(mo, Path):
    default_in = "./test_data/ptv_is.%d" if Path("./test_data").exists() else "../test_data/ptv_is.%d"
    default_out = "./test_zarr/trajectories.zarr" if Path("./test_zarr").exists() else "./run.zarr"

    inName_ui = mo.ui.text(
        full_width=True,
        value=default_in,
        label="Input Data Path (.zarr, ptv_is.%d, or .h5):"
    )

    trajects_out_ui = mo.ui.text(
        full_width=True,
        value=default_out,
        label="Export Zarr Store Name (.zarr):"
    )

    min_length_ui = mo.ui.number(
        full_width=True,
        value=3,
        label="Minimum trajectory length:"
    )

    mo.vstack([inName_ui, trajects_out_ui, min_length_ui])
    return inName_ui, min_length_ui, trajects_out_ui


@app.cell
def _(
    Path,
    inName_ui,
    min_length_ui,
    read_zarr_trajectories,
    save_zarr_trajectories,
    trajectories,
    trajects_out_ui,
):
    inName = inName_ui.value
    trajects_zarr = trajects_out_ui.value

    out_p = Path(trajects_zarr)
    if not out_p.exists():
        trajects = trajectories(inName, traj_min_len=min_length_ui.value)
        save_zarr_trajectories(trajects, trajects_zarr, group="trajectories")
        print(f"Loaded trajectories from '{inName}' and exported Zarr store -> '{trajects_zarr}'")
    else:
        trajects = read_zarr_trajectories(trajects_zarr, group="trajectories")
        if not trajects:
            trajects = trajectories(inName, traj_min_len=min_length_ui.value)
        print(f"Loaded trajectories from Zarr store '{trajects_zarr}' for post-analysis")
    return (trajects,)


@app.cell
def _(mo, plt, trajects):
    # 2. Create a figure and add 3D axes
    fig = plt.figure()
    # The 'projection="3d"' keyword enables the 3D functionality
    ax = fig.add_subplot(111, projection="3d")
    for traj in trajects:
        # Swap y and z to make y vertical (which is the z-axis in matplotlib 3d)
        # x -> x, z -> y (depth), y -> z (vertical)
        ax.plot(traj.pos()[:, 0], traj.pos()[:, 2], traj.pos()[:, 1])

    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_zlabel("y")

    mo.mpl.interactive(fig)
    return


if __name__ == "__main__":
    app.run()
