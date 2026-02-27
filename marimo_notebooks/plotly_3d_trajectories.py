import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    # plotly
    return


@app.cell
def _():
    from flowtracks.io import trajectories_ptvis
    inName = '/Volumes/ExtremePro/test_ed_lab/res/ptv_is.%d'
    trajects = trajectories_ptvis(inName, traj_min_len=15)
    return (trajects,)


@app.cell
def _(trajects):
    trajects[0].pos()
    return


@app.cell
def _(trajects):
    len(trajects)
    return


@app.cell
def _(trajects):
    import pandas as pd
    tmp = []
    for tr in trajects:
        tmp.append(pd.DataFrame({'id':tr.trajid(),'x':tr.pos()[:,0],'y':tr.pos()[:,1],'z':tr.pos()[:,2]}))
    
    
    df = pd.concat(tmp)
    return (df,)


@app.cell
def _(df):
    import plotly.express as px
    # df = px.data.gapminder().query("continent=='Europe'")
    fig = px.line_3d(df, x="x", y="y", z="z", color='id')
    fig.show()
    return


if __name__ == "__main__":
    app.run()
