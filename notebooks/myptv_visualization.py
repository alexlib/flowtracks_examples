# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.20.2",
# ]
# ///
import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from pathlib import Path
    from flowtracks.io import trajectories_ptvis
    from matplotlib.colors import Colormap
    from mpl_toolkits import mplot3d

    # '%matplotlib tk' command supported automatically in marimo
    return Colormap, Path, np, plt, trajectories_ptvis


@app.cell
def _(Path, trajectories_ptvis):

    # Get the directory of this notebook file
    notebook_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    inName = str((notebook_dir / '..' / 'test_data' / 'ptv_is.%d').resolve())
    trajects = trajectories_ptvis(inName, traj_min_len=10)
    return (trajects,)


@app.cell
def _(Colormap, np, plt, trajects):


    cmap: Colormap = plt.get_cmap('viridis')
    fig = plt.figure()
    fig.set_size_inches(9, 7)
    ax = fig.add_subplot(projection='3d')
    for tr_1 in trajects:
        V = np.mean(tr_1.velocity()[:, 0] ** 2 + tr_1.velocity()[:, 1] ** 2 + tr_1.velocity()[:, 2] ** 2) ** 0.5
        color = cmap(V / 0.5)
        ax.plot(tr_1.pos()[:, 0], tr_1.pos()[:, 2], tr_1.pos()[:, 1], color=color)
    ax.set_xlim(-40, 40)
    ax.set_zlim(-40, 40)
    ax.set_ylim(-40, 40)
    plt.tight_layout()
    return (fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Trying a 3D flowing arrows movie:
    """)
    return


@app.cell
def _(fig, plt):
    fig_1 = plt.figure()
    fig_1.set_size_inches(9, 8)
    ax_1 = fig.add_subplot(111, projection='3d')

    plt.tight_layout()

    ax_1.set_xlim(-40, 40)
    ax_1.set_ylim(-40, 40)
    ax_1.set_zlim(-40, 40)
    ax_1.grid(False)

    ax_1.xaxis.pane.set_edgecolor('w')
    ax_1.yaxis.pane.set_edgecolor('w')
    ax_1.zaxis.pane.set_edgecolor('w')
    ax_1.xaxis.pane.fill = False
    ax_1.yaxis.pane.fill = False
    ax_1.zaxis.pane.fill = False
    ax_1.tick_params(axis='x', colors='w')
    ax_1.tick_params(axis='y', colors='w')
    ax_1.tick_params(axis='z', colors='w')
    ax_1.set_xticks([])
    ax_1.set_yticks([])
    ax_1.set_zticks([])
    ax_1.set_facecolor((0.1, 0.0, 0.0))
    fig_1.set_facecolor((0.1, 0.0, 0.0))
    ax_1.set_xlabel('X [mm]', color='w')
    ax_1.set_ylabel('Z [mm]', color='w')
    ax_1.set_zlabel('Y [mm]', color='w')
    return (ax_1,)


@app.cell
def _(ax_1, np, plt, trajects):
    cmap_1 = plt.get_cmap('viridis')
    # Concatenate all trajectory DataFrames to create data_1


    # Animation using flowtracks API
    frames = np.unique(np.concatenate([tr.time() for tr in trajects]))
    N = 3
    for e, frm in enumerate(frames):
        ax_1.clear()
        for tr_2 in trajects:
            mask = (tr_2.time() > frm - N) & (tr_2.time() < frm + N)
            if np.any(mask):
                seg = tr_2.pos()[mask]
    return


app._unparsable_cell(
    r"""
    import numpy as np
    import plotly.graph_objects as go

    fig = go.Figure(
    data=[go.Scatter3d(x=env.xsuc, y=env.ysuc, z=env.zsuc,
    mode=“markers”,marker=dict(color=“darkolivegreen”, size=10)),
    ])




    fig = go.Figure(go.Scatter3d(x=env.xsuc, y=env.ysuc, z=env.zsuc, #this is the trace 0
                            mode='markers',marker=dict(color='darkolivegreen', size=10)))
    fig.add_scatter3d(x=env.x_par, y=env.y_par, z=env.z_par,  #this is the trace 1
                      mode='markers',marker=dict(color='gold', size=10,symbol='square'))
    N = len(env.xsuc)#it must be equal with the len(env.x_par)
    frames = [go.Frame(data= [go.Scatter3d(x=env.xsuc[:k+1],
                                     y=env.ysuc[:k+1],
                                     z=env.zsuc[:k+1]),
                              go.Scatter3d(x=env.x_par[:k+1],
                                y=env.y_par[:k+1],
                                z=env.z_par[:k+1])],
                       name=f'frame{k}',
                       traces=[0,1]) for k in range(N)]  # traces =[0,1] tells plotly.js  that the first element in frame data
                                                         #updates trace 0, while the second the trace 1
    fig.update(frames=frames)
    fig.update_layout(updatemenus=[dict(type='buttons',
                                        buttons=[dict(label='Play',
                                                      method='animate',
                                                      args=[None, 
                                                            dict(frame=dict(redraw=True,
                                                                            fromcurrent=True, 
                                                                            mode=‘immediate’)) ])])])
    fig.update_scenes(xaxis=dict(range=[0.2, 3.8],title="X-axis", autorange=False),
                      yaxis=dict(range=[-0.334,+0.334],title="Y-axis", autorange=False),
                      zaxis=dict(range=[0.7, 1.1],title ="Z-axis", autorange=False))
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
