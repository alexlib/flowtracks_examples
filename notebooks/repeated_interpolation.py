import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Example of flowtracks repeated interpolation method

    As an example of using repeated interpolation at the same place, this notebook performs a consistency-checking process, a simplified version of the method introduced by B. Lüthi [1]

    Our first move is to open the dual (tracers + inertial particles) scene data. If you are not familiar with the DualScene class yet, the notebook ``doc/hdf5_scene_analysis.ipynb`` has the introduction you need.
    """)
    return


@app.cell
def _():
    from flowtracks.scene import Scene
    from pathlib import Path
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    h5_path = base_dir / 'test_h5' / 'traj_GT.h5' if (base_dir / 'test_h5').exists() else base_dir / '..' / 'test_h5' / 'traj_GT.h5'
    scene = Scene(str(h5_path))
    return (scene,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll use Inverse Distance Weighting, so as not to weigh down the computation. Furthermore, we tell the interpolant to select candidate tracers within a certain radius. Inside this radius, we'll be able to take subsamples of any size, as we'll later see.
    """)
    return


@app.cell
def _():
    from flowtracks.interpolation import Interpolant
    interp = Interpolant('inv', None, radius=0.010, param=1.5)
    return (interp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's find a nice frame and pick a particle with enough tracers around it (at least 3 in this case).
    """)
    return


@app.cell
def _(interp, scene):
    import numpy as np

    for frame in scene.iter_frames():
        if len(frame) == 0:
            continue
        interp.set_scene(frame.pos(), frame.pos(), frame.velocity())
        neighb_base = interp.which_neighbours()
        candidates = neighb_base.sum(axis=1) >= 3
        if candidates.any():
            break
    return candidates, frame, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Anyway, we have a particle. So now we can tell the interpolant that from now on, this will be the only interpolation point, by giving a mask containing only one True value.
    """)
    return


@app.cell
def _(candidates, interp, np):
    selector = np.ones_like(candidates)
    selector[candidates.nonzero()[0][0]] = False
    interp.trim_points(selector)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now the gist of the method is that we go over different combinations of particles and check the standard deviation of interpolation results, compared to their RMS.
    """)
    return


@app.cell
def _(interp, np):
    from scipy.special import comb

    num_combs = int(min([50, comb(10, 4, exact=True)]))
    samples = np.empty((num_combs, 3))

    neighb_base = interp.which_neighbours()
    where_active = np.nonzero(neighb_base[0])[0]
    neighb_comb = np.empty_like(neighb_base)

    if len(where_active) > 0:
        for cix in range(num_combs):
            neighb_comb[...] = False
            k = min(4, len(where_active))
            neighb_ix = np.random.choice(where_active, size=k, replace=False)
            neighb_comb[0, neighb_ix] = True
            samples[cix] = interp.interpolate(neighb_comb)

        rms = np.linalg.norm(samples, axis=0) / np.sqrt(num_combs)
        rel_std = np.std(samples, axis=0) / (rms + 1e-12)
        print("Relative standard deviation: " + str(rel_std))
    else:
        print("No active neighbours found for repeated interpolation sample.")
    return



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Well, this particle seems to have relatively inconsistent fluid velocity interpolation, although in the Y coordinate prediction is more consistent than the others. Well then. Let's not get discouraged: there are many more particles in the data set, and surely by averaging over all of them, we can find the true consistency of the data set. But this is not for a short tutorial like this.

    ##References:
    [1] B. Lüthi et al., Lagrangian multi-particle statistics, 2007, DOI:
    10.1080/14685240701522927
    """)
    return


if __name__ == "__main__":
    app.run()
