import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    from flowtracks.io import Scene
    import numpy as np

    # install plotly express https://plot.ly/python/getting-started/
    import plotly.express as px
    import pandas as pd

    return Scene, np, pd, px


@app.cell
def _(Scene):
    particles = Scene('./test_h5/traj_GT.h5')
    return (particles,)


@app.cell
def _(np, particles, pd):
    pos,vel = [],[]
    for id in particles.trajectory_ids():
        tr = particles.trajectory_by_id(id)
        pos.append(np.c_[tr.pos()[:,0],tr.pos()[:,1],tr.pos()[:,2]])
        vel.append(np.c_[tr.velocity()[:,0],tr.velocity()[:,1],tr.velocity()[:,2]])

    df = pd.DataFrame(np.c_[np.vstack(pos),np.vstack(vel)])
    df.columns = ['x','y','z','u','v','w']
    df['vel'] = np.sqrt(df['u']**2+df['v']**2+df['w']**2)
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df, px):
    fig = px.scatter_3d(df,x='x',y='y',z='z',color=df.vel, opacity=0.5)

    fig.show()
    return


if __name__ == "__main__":
    app.run()
