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
        trajectories_ptvis,
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
        save_particles_table,
        trajectories_ptvis,
        trajectories_table,
    )


@app.cell
def _(mo):
    inName_ui = mo.ui.text(
        full_width=True,
        value="./pyPTV_folder/res/ptv_is.%d",
        label="inName:"
    )

    trajects_hdf_ui = mo.ui.text(
        full_width=True,
        value="./pyPTV_folder/trajectories.h5",
        label="Save file name:"
    )

    min_length_ui = mo.ui.number(
        full_width=True,
        value=50,
        label="Minimum trajectory length:"
    )

    mo.vstack([inName_ui, trajects_hdf_ui, min_length_ui])
    return inName_ui, min_length_ui, trajects_hdf_ui


@app.cell
def _(
    Path,
    inName_ui,
    min_length_ui,
    save_particles_table,
    trajectories_ptvis,
    trajectories_table,
    trajects_hdf_ui,
):
    inName = inName_ui.value
    trajects_hdf = trajects_hdf_ui.value

    # print(Path(trajects_hdf).exists())

    if not Path(trajects_hdf).exists():
        trajects = trajectories_ptvis(inName, traj_min_len=min_length_ui.value)
        save_particles_table(trajects_hdf, trajects)
        print("Loaded from /res and saved to hdf5")
    else:
        trajects = trajectories_table(trajects_hdf)
        print("Loaded using flowtracks")
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
