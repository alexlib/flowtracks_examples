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
    import numpy as np
    import matplotlib.pyplot as plt
    # '%matplotlib inline' command supported automatically in marimo
    import flowtracks
    from flowtracks import io

    return io, np, plt


@app.cell
def _(io):
    # get frames where trajectories appeared 
    from pathlib import Path as _Path
    _base_dir = _Path(__file__).parent if '__file__' in globals() else _Path.cwd()
    _data_dir = _base_dir if (_base_dir / 'test_data').exists() else _base_dir / '..' / 'test_data'
    inName = str(_data_dir / 'ptv_is.%d')
    frames_range = [int(tr.time()[-1]) for tr in io.iter_trajectories_ptvis(inName)]
    print(frames_range[0],frames_range[-1])
    return (inName,)


@app.cell
def _(inName, io):
    max_frame = 101010
    trajectories = [tr for tr in io.iter_trajectories_ptvis(inName) if tr.time()[-1] <= max_frame]
    print(f"{len(trajectories)} trajectories")
    return (trajectories,)


@app.cell
def _(mo, trajectories):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("XY Projection", "YZ Projection")
    )

    for tr in trajectories:
        p = tr.pos()
        fig.add_trace(
            go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines+markers", marker=dict(size=3), showlegend=False),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=p[:, 1], y=p[:, 2], mode="lines+markers", marker=dict(size=3), showlegend=False),
            row=1, col=2
        )

    fig.update_layout(title="Multi-Panel 2D Frame Snapshots (Plotly)", height=450)
    mo.ui.plotly(fig)
    return


@app.cell
def _(mo, trajectories):
    import plotly.graph_objects as go

    fig = go.Figure()
    for traj in trajectories:
        p = traj.pos()
        fig.add_trace(
            go.Scatter3d(x=p[:, 0], y=p[:, 1], z=p[:, 2], mode="lines", line=dict(width=4), showlegend=False)
        )

    fig.update_layout(
        title="3D Frame Snapshot Trajectories (Plotly)",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        height=550,
    )
    mo.ui.plotly(fig)
    return



@app.cell
def _():
    # from flowtracks.io import save_particles_table
    return


@app.cell
def _():
    # save_particles_table('test.h5',trajectories)
    return


@app.cell
def _():
    # from flowtracks.scene import Scene
    from flowtracks.scene import Scene
    from flowtracks.graphics import pdf_graph

    return Scene, pdf_graph


@app.cell
def _(Scene):
    from pathlib import Path as _Path
    _base_dir = _Path(__file__).parent if '__file__' in globals() else _Path.cwd()
    _h5_path = _base_dir / 'test_h5' / 'traj_RC.h5' if (_base_dir / 'test_h5').exists() else _base_dir / '..' / 'test_h5' / 'traj_RC.h5'
    scn = Scene(str(_h5_path))
    return (scn,)


@app.cell
def _(np, pdf_graph, plt, scn):
    # Plot distribution of trajectory lengths
    frames = 0.
    for frame in scn.iter_frames():
        frames += 1

    lens = np.array([len(trj) for trj in scn.iter_trajectories()])
    pdf_graph(lens/frames*100, 20, log_density=True)

    plt.xlabel("Traj. len [% of scene length]")
    plt.ylabel("Probability density")
    # plt.legend(legends)
    plt.grid()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
