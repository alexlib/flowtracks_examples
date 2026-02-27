import marimo

__generated_with = "0.20.2"
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

    # '%matplotlib tk' command supported automatically in marimo
    return np, pd, plt


@app.cell
def _(pd):
    names=['traj', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'ax', 'ay', 'az', 't']
    data = pd.read_csv('/Users/alex/Documents/repos/myptv/with_MyPTV/smoothed_trajectories', 
                       delimiter='\t', names = names, header=None)
    return (data,)


@app.cell
def _(data):
    data_1 = data[data['traj'] != -1]
    return (data_1,)


@app.cell
def _(data_1):
    ids = list(set(data_1['traj']))
    # ids.remove(-1)
    len(ids)
    return (ids,)


@app.cell
def _(data_1, ids):
    longs = []
    for i in ids:
        tr = data_1[data_1['traj'] == i]
        if len(tr) > 25:
            longs.append(tr)
    print(len(longs))
    return (longs,)


@app.cell
def _(longs, np, plt):
    from mpl_toolkits import mplot3d
    import matplotlib
    cmap = matplotlib.cm.get_cmap('winter')
    fig = plt.figure()
    fig.set_size_inches(9, 7)
    ax = fig.add_subplot(projection='3d')
    for tr_1 in longs:
        V = np.mean(tr_1['vx'] ** 2 + tr_1['vy'] ** 2 + tr_1['vz'] ** 2) ** 0.5
        color = cmap(V / 0.5)
        ax.plot(tr_1['x'], tr_1['z'], tr_1['y'], color=color)
    ax.set_xlim(-40, 40)
    ax.set_zlim(-40, 40)
    ax.set_ylim(-40, 40)
    # fig.savefig('trajs.pdf')
    plt.tight_layout()
    return (matplotlib,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Trying a 3D flowing arrows movie:
    """)
    return


@app.cell
def _(matplotlib, plt):
    fig_1 = plt.figure()
    fig_1.set_size_inches(9, 8)
    ax_1 = plt.axes(projection='3d')
    plt.tight_layout()
    ax_1.set_xlim(-40, 40)
    ax_1.set_zlim(-40, 40)
    ax_1.set_ylim(-40, 40)
    ax_1.grid(False)
    ax_1.xaxis.pane.set_edgecolor('w')
    ax_1.yaxis.pane.set_edgecolor('w')
    ax_1.zaxis.pane.set_edgecolor('w')
    ax_1.xaxis.pane.fill = False
    ax_1.yaxis.pane.fill = False
    ax_1.zaxis.pane.fill = False
    matplotlib.rc('axes', edgecolor='w')
    ax_1.tick_params(axis='x', colors='w')
    ax_1.tick_params(axis='y', colors='w')
    ax_1.tick_params(axis='z', colors='w')
    ax_1.w_xaxis.line.set_color('w')
    ax_1.w_yaxis.line.set_color('w')
    ax_1.w_zaxis.line.set_color('w')
    ax_1.set_xticks([])
    ax_1.set_yticks([])
    ax_1.set_zticks([])
    ax_1.set_facecolor((0.1, 0.0, 0.0))
    fig_1.set_facecolor((0.1, 0.0, 0.0))
    return ax_1, fig_1


@app.cell
def _(ax_1, data_1, fig_1, longs, matplotlib, np):
    cmap_1 = matplotlib.cm.get_cmap('winter')
    frames = list(set(data_1['t']))
    N = 5
    for e, frm in enumerate(frames[:]):
        ax_1.clear()
        for tr_2 in longs:
            tr_seg = tr_2[(tr_2['t'] > frm - N) & (tr_2['t'] < frm + N)]
            V_1 = np.mean(tr_2['vx'] ** 2 + tr_2['vy'] ** 2 + tr_2['vz'] ** 2) ** 0.5
            ax_1.plot(tr_seg['x'], tr_seg['z'], tr_seg['y'], color=cmap_1((V_1 - 0.05) / 0.25))
        ax_1.set_xlim(-40, 40)
        ax_1.set_zlim(-40, 40)
        ax_1.set_ylim(-40, 40)
        ax_1.grid(False)
        ax_1.xaxis.pane.set_edgecolor('w')
        ax_1.yaxis.pane.set_edgecolor('w')
        ax_1.zaxis.pane.set_edgecolor('w')
        ax_1.xaxis.pane.fill = False
        ax_1.yaxis.pane.fill = False
        ax_1.zaxis.pane.fill = False
        ax_1.w_xaxis.line.set_color('w')  #ax.set_xlabel('x [mm]')
        ax_1.w_yaxis.line.set_color('w')  #ax.set_ylabel('z [mm]')
        ax_1.w_zaxis.line.set_color('w')  #ax.set_zlabel('y [mm]')
        ax_1.set_xticks([])
        ax_1.set_yticks([])
        ax_1.set_zticks([])
        fig_1.savefig('./img/im%03d.jpg' % e)
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
