import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # attempt to read trajectories data from Alex Ruiz
    """)
    return


@app.cell
def _():
    import numpy as np
    # from scipy.io import loadmat
    import matplotlib.pyplot as plt
    # '%matplotlib inline' command supported automatically in marimo
    return np, plt


@app.cell
def _():
    import flowtracks
    import hdf5storage
    import os
    from flowtracks.trajectory import Trajectory

    return Trajectory, hdf5storage, os


@app.cell
def _():
    # For other MAT format, not v7.3 (HDF5)
    # from flowtracks.io import trajectories_mat
    # traj = trajectories_mat('traj_GT.mat')
    return


@app.cell
def _(Trajectory, hdf5storage, np, os):
    def trajectories_mat_73(fname, data_name=None):
        """
        Extracts all trajectories from a Matlab file. the file is formated as a 
        list of trajectory record arrays, containing attributes 'xf', 'yf', 'zf'
        for position, 'uf', 'vf', 'wf' for velocity, and 'axf', 'ayf', 'azf' for
        acceleration.
    
        Modified by Alex Liberzon for v7.3 MAT files that cannot be loaded by
        scipy.io.loadmat but nicely by hdf5storage, e.g.:
    
        
            $ pip install hdf5storage
        
            trajects = trajectories_mat_73(fname)

    
        Arguments:
        fname - path to the Matlab file.
    
        Returns:
        trajects - a list of :class:`~flowtracks.trajectory.Trajectory` objects,
            one for each trajectory contained in the mat file.
        """
        data = hdf5storage.loadmat(os.path.expanduser(fname))
        if data_name is None:
            data_name = [s for s in data.keys() if not s.startswith('__') and (not s == 'directory')][0]
        raw = np.hstack(data[data_name][0])  # Get the workspace variable holding the trajectories:
        trajects = []
        for _traj in raw:
            pos = np.hstack((_traj['xf'], _traj['yf'], _traj['zf']))
            vel = np.hstack((_traj['uf'], _traj['vf'], _traj['wf']))
            accel = np.hstack((_traj['axf'], _traj['ayf'], _traj['azf']))
            t = _traj['t'].squeeze()
            trajid = _traj['trajid'][0, 0]
            trajects.append(Trajectory(pos, vel, t, trajid, accel=accel))  # also convert data from mm to m.
        return trajects  # /1000. apparently it's already in mm  #/1000.  # /1000.

    return (trajectories_mat_73,)


@app.cell
def _(trajectories_mat_73):
    trajects_GT = trajectories_mat_73('traj_GT.mat')
    return (trajects_GT,)


@app.cell
def _(plt, trajects_GT):
    for _traj in trajects_GT:
        plt.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], '.')  # traj is a Trajectory object, supplied by the
    plt.show()  # flowtracks.trajectory module.
    return


@app.cell
def _(trajectories_mat_73):
    trajects_RC = trajectories_mat_73('traj_RC.mat',data_name='traj')
    return (trajects_RC,)


@app.cell
def _(plt, trajects_RC):
    for _traj in trajects_RC:
        plt.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], '.')  # traj is a Trajectory object, supplied by the
    plt.show()  # flowtracks.trajectory module.
    return


if __name__ == "__main__":
    app.run()
