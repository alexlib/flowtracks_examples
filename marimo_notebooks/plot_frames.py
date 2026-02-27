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
    frames_range = [int(tr.time()[-1]) for tr in io.iter_trajectories_ptvis('./test_data/ptv_is.%d')]
    print(frames_range[0],frames_range[-1])
    return


@app.cell
def _(io):
    max_frame = 101010
    trajectories = [tr for tr in io.iter_trajectories_ptvis('./test_data/ptv_is.%d') if tr.time()[-1] <= max_frame]
    print(f"{len(trajectories)} trajectories")
    return (trajectories,)


@app.cell
def _(plt, trajectories):
    _fig, _ax = plt.subplots(1, 2, figsize=(12, 5))
    for tr in trajectories:
        _ax[0].plot(tr.pos()[:, 0], tr.pos()[:, 1])
        _ax[0].plot(tr.pos()[0, 0], tr.pos()[0, 1], '.')
        _ax[0].set_xlabel('$x$', fontsize=16)
        _ax[0].set_ylabel('$y$', fontsize=16)
        _ax[1].plot(tr.pos()[:, 1], tr.pos()[:, 2])
        _ax[1].plot(tr.pos()[0, 1], tr.pos()[0, 2], '.')
        _ax[1].set_xlabel('$y$', fontsize=16)
        _ax[1].set_ylabel('$z$', fontsize=16)
    return


@app.cell
def _(plt, trajectories):
    from mpl_toolkits.mplot3d import Axes3D
    _fig = plt.figure(figsize=(8, 6))
    _ax = _fig.add_subplot(111, projection='3d')
    for traj in trajectories:
        _ax.plot(traj.pos()[:, 0], traj.pos()[:, 1], traj.pos()[:, 2], '-', lw=3)
        _ax.set_xlabel('$x$', fontsize=16)
        _ax.set_ylabel('$y$', fontsize=16)
        _ax.set_zlabel('$z$', fontsize=16)
    plt.show()
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
    # from flowtracks.io import Scene
    from flowtracks.scene import Scene
    from flowtracks.graphics import pdf_graph

    return Scene, pdf_graph


@app.cell
def _(Scene):
    scn = Scene('./test_h5/traj_RC.h5')
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
