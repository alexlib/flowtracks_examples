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
    # plotly
    return


@app.cell
def _():
    from flowtracks.io import trajectories, read_zarr_trajectories
    from pathlib import Path
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    zarr_path = base_dir / 'test_zarr' / 'trajectories.zarr' if (base_dir / 'test_zarr').exists() else base_dir / '..' / 'test_zarr' / 'trajectories.zarr'
    data_dir = base_dir if (base_dir / 'test_data').exists() else base_dir / '..' / 'test_data'

    if zarr_path.exists():
        inName = str(zarr_path)
    else:
        inName = str(data_dir / 'ptv_is.%d')

    trajects = trajectories(inName, traj_min_len=5)
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
