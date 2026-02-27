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
    import h5py
    import os
    from flowtracks.trajectory import Trajectory

    return Trajectory, h5py, os


@app.cell
def _(Trajectory, h5py, np, os):
    def trajectories_mat_h5py(fname):
        """
        Extracts all trajectories from a Matlab file. the file is formated as a 
        list of trajectory record arrays, containing attributes 'xf', 'yf', 'zf'
        for position, 'uf', 'vf', 'wf' for velocity, and 'axf', 'ayf', 'azf' for
        acceleration.

        Modified by Alex Liberzon for v7.3 MAT files that cannot be loaded by
        scipy.io.loadmat but nicely by h5py:


            trajects = trajectories_mat_h5py(fname)


        Arguments:
        fname - path to the Matlab file.

        Returns:
        trajects - a list of :class:`~flowtracks.trajectory.Trajectory` objects,
            one for each trajectory contained in the mat file.
        """

        with h5py.File(os.path.expanduser(fname),'r+') as f:

            # Get the workspace variable holding the trajectories:
            data_name = [s for s in f.keys() \
                if (not s.startswith('__')) and (not s == '#refs#')][0]
            # raw = np.hstack(data[data_name][0])

            ref = f[data_name] # reference only

            trajects = []

            # horizontal or vertical structure:

            if np.argmax(ref['t'].shape) == 0:

                for i in range(ref['t'].shape[0]):
                    # also convert data from mm to m.
                    pos = np.vstack((f[ref['xf'][i][0]][()],f[ref['yf'][i][0]][()],f[ref['zf'][i][0]][()])).T
                    vel = np.vstack((f[ref['uf'][i][0]][()],f[ref['vf'][i][0]][()],f[ref['wf'][i][0]][()])).T
                    accel = np.vstack((f[ref['axf'][i][0]][()],f[ref['ayf'][i][0]][()],f[ref['azf'][i][0]][()])).T
                    t = f[ref['t'][i][0]][()].squeeze()
                    trajid = f[ref['trajid'][i][0]][()][0][0]
                    trajects.append(Trajectory(pos, vel, t, trajid, accel=accel))

            else:

                for i in range(ref['t'].shape[-1]):
                    # also convert data from mm to m.
                    pos = np.vstack((f[ref['xf'][0][i]][()],f[ref['yf'][0][i]][()],f[ref['zf'][0][i]][()])).T
                    vel = np.vstack((f[ref['uf'][0][i]][()],f[ref['vf'][0][i]][()],f[ref['wf'][0][i]][()])).T
                    accel = np.vstack((f[ref['axf'][0][i]][()],f[ref['ayf'][0][i]][()],f[ref['azf'][0][i]][()])).T
                    t = f[ref['t'][0][i]][()].squeeze()
                    trajid = f[ref['trajid'][0][i]][()][0][0]
                    trajects.append(Trajectory(pos, vel, t, trajid, accel=accel))

        return trajects

    return (trajectories_mat_h5py,)


@app.cell
def _(trajectories_mat_h5py):
    trajects_GT = trajectories_mat_h5py('./test_mat/traj_GT.mat')
    return (trajects_GT,)


@app.cell
def _(plt, trajects_GT):
    for _traj in trajects_GT:
        plt.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], '.')  # traj is a Trajectory object, supplied by the
    plt.show()  # flowtracks.trajectory module.
    return


@app.cell
def _(trajectories_mat_h5py):
    trajects_RC = trajectories_mat_h5py('./test_mat/traj_RC.mat')
    return (trajects_RC,)


@app.cell
def _(plt, trajects_RC):
    for _traj in trajects_RC:
        plt.plot(_traj.pos()[:, 0], _traj.pos()[:, 1], '.')  # traj is a Trajectory object, supplied by the
    plt.show()  # flowtracks.trajectory module.
    return


@app.cell
def _(trajects_GT, trajects_RC):
    from flowtracks.io import save_particles_table
    save_particles_table('traj_GT.h5',trajects_GT)
    save_particles_table('traj_RC.h5',trajects_RC)
    return


if __name__ == "__main__":
    app.run()
