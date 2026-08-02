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
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    if (base_dir / 'test_data').exists():
        inName = str((base_dir / 'test_data' / 'ptv_is.%d').resolve())
    elif (base_dir / '..' / 'test_data').exists():
        inName = str((base_dir / '..' / 'test_data' / 'ptv_is.%d').resolve())
    else:
        inName = './test_data/ptv_is.%d'

    trajects = trajectories_ptvis(inName, traj_min_len=10)
    return (trajects,)


@app.cell
def _(mo, np, trajects):
    import plotly.graph_objects as go

    fig = go.Figure()
    v_max = 0.5
    for tr in trajects:
        vel = tr.velocity()
        if len(vel) > 0:
            speed = np.linalg.norm(vel, axis=1)
            mean_speed = np.mean(speed)
        else:
            mean_speed = 0.0

        p = tr.pos()
        fig.add_trace(
            go.Scatter3d(
                x=p[:, 0],
                y=p[:, 1],
                z=p[:, 2],
                mode="lines+markers",
                marker=dict(
                    size=3,
                    color=speed if len(vel) > 0 else "blue",
                    colorscale="Viridis",
                    cmin=0,
                    cmax=v_max,
                    showscale=False,
                ),
                line=dict(
                    color=f"rgb({int(255*min(1.0, mean_speed/v_max))}, 100, 200)",
                    width=3,
                ),
                name=f"ID {tr.trajid()}",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Speed-Colormapped 3D Trajectories (Plotly Viridis)",
        scene=dict(xaxis_title="X [mm]", yaxis_title="Y [mm]", zaxis_title="Z [mm]"),
        height=600,
    )

    mo.ui.plotly(fig)
    return



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Trying a 3D flowing arrows movie:
    """)
    return


@app.cell
def _(plt):
    fig_1 = plt.figure()
    fig_1.set_size_inches(9, 8)
    ax_1 = fig_1.add_subplot(111, projection='3d')

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


@app.cell
def _():
    # Note: env is not defined in this notebook, so this cell is kept as a commented reference.
    # To run this, env must be defined.
    """
    import numpy as np
    import plotly.graph_objects as go

    fig = go.Figure(
    data=[go.Scatter3d(x=env.xsuc, y=env.ysuc, z=env.zsuc,
    mode="markers",marker=dict(color="darkolivegreen", size=10)),
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
                                                                            mode='immediate')) ])])])
    fig.update_scenes(xaxis=dict(range=[0.2, 3.8],title="X-axis", autorange=False),
                      yaxis=dict(range=[-0.334,+0.334],title="Y-axis", autorange=False),
                      zaxis=dict(range=[0.7, 1.1],title ="Z-axis", autorange=False))
    """
    return


if __name__ == "__main__":
    app.run()
