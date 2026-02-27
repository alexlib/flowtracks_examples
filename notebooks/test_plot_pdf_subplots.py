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
    from flowtracks.io import iter_trajectories_ptvis
    from mpl_toolkits.mplot3d import Axes3D

    return iter_trajectories_ptvis, np, plt


@app.cell
def _():
    # see openptv forum for Christophe Henry messages
    inName = "./test_data/ptv_is.%d" 
    # or use the test data
    # inName = "./test_data/ptv_is.%d" # the directory with the input files
    return (inName,)


@app.cell
def _(inName, iter_trajectories_ptvis):
    #----parameters
    traj_min_len = 10 # in this particular example we have short trajectories

    #----cal traj.
    trajects = list(iter_trajectories_ptvis(inName, first=101000, last=101025, traj_min_len=traj_min_len))
    return (trajects,)


@app.cell
def _(trajects):
    print(f"{len(trajects)} trajectories")
    return


@app.cell
def _(plt, trajects):


    _fig = plt.figure(figsize=(12, 10))
    ax = _fig.add_subplot(111, projection='3d')
    for _tr in trajects:  # generate one trajectory per loop call
        plt.plot(_tr.pos()[:, 0], _tr.pos()[:, 1], _tr.pos()[:, 2], '-o')
    return


@app.cell
def _(trajects):
    u, v, w = ([], [], [])
    ax_1, ay, az = ([], [], [])
    for _tr in trajects:
        u.append(_tr.velocity()[:, 0])
        v.append(_tr.velocity()[:, 1])
        w.append(_tr.velocity()[:, 2])
        ax_1.append(_tr.accel()[:, 0])
        ay.append(_tr.accel()[:, 1])
        az.append(_tr.accel()[:, 2])
    return ax_1, ay, az, u, v, w


@app.cell
def _(ax_1, ay, az, np, plt, u, v, w):
    _fig, a = plt.subplots(1, 2, figsize=(10, 8))
    a[0].hist(np.hstack(u), 100, alpha=0.1)
    a[0].hist(np.hstack(v), 100, alpha=0.1)
    a[0].hist(np.hstack(w), 100, alpha=0.1)
    a[1].hist(np.hstack(ax_1), 100, alpha=0.1)
    a[1].hist(np.hstack(ay), 100, alpha=0.1)
    a[1].hist(np.hstack(az), 100, alpha=0.1)
    a[0].set_xlim(-0.005, 0.005)
    a[1].set_xlim(-0.001, 0.001)
    return


@app.cell
def _(np, plt):
    def plot_vel_pdfs(traj_list, fit_gaussian=True, bins=100, bin_range=None, ax=None):
        """
        will generate a pdf of trajectory vecolicties and if specified 
        by (fit_gaussian = True) will fit a gaussian to the data
        """
        vx, vy, vz = ([], [], [])
        M = -1.0
        for i in traj_list:
            v = i.velocity()
            for j in range(v.shape[0]):
                vx.append(v[j, 0])
                vy.append(v[j, 1])
                vz.append(v[j, 2])
            if np.amax(np.abs(v)) > M:
                M = np.amax(np.abs(v))
        if bin_range == None:
            bin_range = (-M, M)
        if ax is None:
            _fig, ax = plt.subplots()
        else:
            _fig = ax.get_figure()
        c = ['b', 'r', 'g']
        shp = ['o', 'd', 'v']
        lbl = ['$v_x$', '$v_y$', '$v_z$']
        for e, i in enumerate([vx, vy, vz]):
            h = np.histogram(i, bins=bins, density=True, range=bin_range)
            x, y = (0.5 * (h[1][:-1] + h[1][1:]), h[0])
            m, s = (np.mean(i), np.std(i))
            xx = np.arange(-M, M, 2.0 * M / 500)
            ax.plot(x, y, c[e] + shp[e] + '-', lw=0.4, label=lbl[e] + ' $\\mu = %.3f$ $\\sigma = $%0.3f' % (m, s))
            if fit_gaussian:
                ax.plot(xx, gaussian(xx, m, s), c[e], lw=1.2)
        ax.legend()
        ax.set_xlabel('$v_i$')
        ax.set_ylabel('P($v_i$)')
        return (_fig, ax)

    def gaussian(x, m, s):
        return 1.0 / np.sqrt(2 * np.pi) / s * np.exp(-0.5 * ((x - m) / s) ** 2)

    return (plot_vel_pdfs,)


@app.cell
def _(plot_vel_pdfs, trajects):
    plot_vel_pdfs(trajects)
    return


@app.cell
def _(plot_vel_pdfs, trajects):
    fig1,ax1 = plot_vel_pdfs(trajects); fig2,ax2 = plot_vel_pdfs(trajects);
    return


@app.cell
def _(plot_vel_pdfs, plt, trajects):
    _fig, ax_2 = plt.subplots(1, 2, figsize=(8, 4))
    plot_vel_pdfs(trajects, ax=ax_2[0])
    plot_vel_pdfs(trajects, ax=ax_2[1])
    return


if __name__ == "__main__":
    app.run()
