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
def _(mo, trajects):
    import plotly.graph_objects as go

    fig = go.Figure()
    for traj in trajects:
        p = traj.pos()
        fig.add_trace(
            go.Scatter3d(
                x=p[:, 0],
                y=p[:, 1],
                z=p[:, 2],
                mode="lines+markers",
                marker=dict(size=2),
                name=f"ID {traj.trajid()}",
                showlegend=False,
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        title="Interactive 3D Trajectories (Plotly)",
        height=600,
    )

    mo.ui.plotly(fig)
    return



if __name__ == "__main__":
    app.run()
