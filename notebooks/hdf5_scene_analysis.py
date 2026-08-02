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
    This tutorial goes through the steps of taking a dual scene (that is, a scene containing synchronous measurements of tracers and inertial particles in the same volume) and exploring and analysing the data.

    We start with just the inertial particles. Our example data is stored in the postptv repository, in the ``data/`` subdirectory. We open it like so:
    """)
    return


@app.cell
def _():
    from flowtracks.scene import Scene
    from pathlib import Path
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    h5_path = base_dir / 'test_h5' / 'traj_GT.h5' if (base_dir / 'test_h5').exists() else base_dir / '..' / 'test_h5' / 'traj_GT.h5'
    particles = Scene(str(h5_path))
    return (particles,)



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The ``Scene`` object allows us to iterate over the data, either trajectory by trajectory, or frame by frame. As an example of trajectory iteration, let's display a 2D view of the existing trajectories.
    """)
    return


@app.cell
def _(particles):
    import matplotlib.pyplot as pl  # Plotting package
    # Show results in the notebook:
    # '%matplotlib inline' command supported automatically in marimo

    for traj in particles.iter_trajectories():
        # traj is a Trajectory object, supplied by the
        # flowtracks.trajectory module.
        pl.plot(traj.pos()[:,0], traj.pos()[:,1], '.')

    pl.show()
    return (pl,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This was easy. However, for large data sets this may be slow. I found that for most analyses it is better to iterate by frames, because we have far less frames than trajectories, and so the chunks that are being processed at each iteration are larger. Additionally, a lot of things you want to know require knowledge about the frame in which the particle is, and not just about the trajectory.

    As an example, we'll find a nicely spaced frame, and show a quiver plot of particle positions and velocities.
    """)
    return


@app.cell
def _(particles, pl):
    for _frame in particles.iter_frames():
        if len(_frame) == 40:  # frame is a ParticleSnapshot object, supplied by the
            pl.quiver(_frame.pos()[:, 0], _frame.pos()[:, 1], _frame.velocity()[:, 0], _frame.velocity()[:, 1])  # flowtracks.trajectory module.
            break
    pl.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you can see, our observation volume is about 3x3 centimeters, and there seems to be more going on on the upper side than the lower one - in this frame. We don't know what will happen in the next - this is turbulence!

    Finally, a concept we will explore in the next section, is iteration over *segments* - pairs of consecutive frames, each containing only the trajectories that are also found in the other.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A dual scene
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now to analyse a dual scene. This is not much different. However, the scene requires, in addition to the data sources on particles and tracers, some more description: the particle properties and the common flow rate are required. So one way to create a dual scene, like the one we have in the ``data/`` directory, is to provide it straight:
    """)
    return


@app.cell
def _():
    from flowtracks.scene import DualScene
    from flowtracks.particle import Particle

    part = Particle(500e-6, 1450) # diameter [m], density [kg/m^3]
    scene = DualScene('../data/particles.h5', '../data/tracers.h5', frate=500, particle=part)
    # It is also possible to set a frame range other than all frames, see the docstring.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, it is easier to use a configuration file containing all the data. Such a file is available in the ``data`` directory as an example:
    """)
    return


@app.cell
def _():
    # cat ../data/seq_hdf.cfg
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the file refers to relative paths, so we'll first switch to the data directory. In your code, you should probably use absolute paths.
    """)
    return


@app.cell
def _():
    import os
    os.chdir('../data')
    from flowtracks.scene import read_dual_scene
    scene_1 = read_dual_scene('../data/seq_hdf.cfg')
    return (scene_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can do calculations that relate both the tracers and the particles. Here, for example, we'll find the fluid velocity around each particle by interpolation from tracers. Like in the above example, Iteration is used to find an arbitrary frame according to some condition (here the number of particles is checked, just because it gives a nice plot). Then the fluid velocity is calculated and the quiver plot is painted so that the least tracer-like inertial particle is red, and the most tracer-like is blue. [note however that the scaling is misleading, the blue particles are not necessarily very good tracers]
    """)
    return


@app.cell
def _(pl, scene_1):
    from numpy.linalg import norm
    from flowtracks.interpolation import Interpolant
    interp = Interpolant('inv', 4, 1)
    for _frame, next_frame in scene_1.iter_segments():
        if len(_frame.particles) == 40:
            vel_interp = interp(_frame.tracers.pos(), _frame.particles.pos(), _frame.tracers.velocity())
            _rel_vel = _frame.particles.velocity() - vel_interp
            c = norm(_rel_vel, axis=1)
            c = c / max(c)
            pos = _frame.particles.pos()
            vel = _frame.particles.velocity()
            pl.quiver(pos[:, 0], pos[:, 1], vel[:, 0], vel[:, 1], c)
            break
    pl.show()
    return interp, norm


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analysis machinery
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A loop such as the one above can be a recurring theme in our analysis code. Furthermore, we would like to read the file only once, and lump all analyses together. For this reason, the module  ``flowtrack.analysis`` exists. It provides the ``analysis()`` function, which iterates over segments, applying user-supplied analysers. An analyser is a class that describes how an analysis is to be made, and what results are to be expected from it. Here, for example, is an analyser implementing the interpolation we have seen above, for a user-defined interpolant:
    """)
    return


@app.cell
def _():
    from flowtracks.analysis import GeneralAnalyser

    class FluidVelocitiesAnalyser(GeneralAnalyser):

        def __init__(self, interp):
            """
            Arguments:
            interp - the Interpolant object to use for finding velocities.
            """
            self._interp = interp

        def descr(self):
            """
            Return a list of two tuples, each of the form 
            (name, data type, row length), describing the arrays returned by 
            analyse() for fluid velocity and relative velocity.
            """
            return [('fluid_vel', float, 3), ('rel_vel', float, 3)]

        def analyse(self, frame, next_frame):
            """
            Arguments:
            frame, next_frame - the Frame object for the currently-analysed frame
                and the one after it, respectively.
        
            Returns:
            a list of two arrays, each of shape (f,3) where f is the number of 
            particles in the current frame. 1st array - fluid velocity. 2nd array
            - relative velocity.
            """
            vel_interp = self._interp(_frame.tracers.pos(), _frame.particles.pos(), _frame.tracers.velocity())
            _rel_vel = _frame.particles.velocity() - vel_interp
            return [vel_interp, _rel_vel]

    return (FluidVelocitiesAnalyser,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note the return values of ``analyse()`` are described by ``descr()``. You can find this class too in ``flowtracks.analysis``. An example of how to use it can be found in ``scripts/analyse_fhdf.py``. We'll run the same example with our own values:
    """)
    return


@app.cell
def _(FluidVelocitiesAnalyser, interp, scene_1):
    from flowtracks.analysis import analysis
    analysis(scene_1, 'results_an.h5', 'seq_hdf.cfg', [FluidVelocitiesAnalyser(interp)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This created a file called 'results_an.h5' in our working directory. It is another HDF file with the analysis results. Now we need to load this analysis in order to look at the results. After loading, any result column can be pulled out in full or partially. We can use this to plot a PDF of the relative velocity.
    """)
    return


@app.cell
def _(norm):
    from flowtracks.an_scene import AnalysedScene
    an_res = AnalysedScene('results_an.h5')
    _rel_vel = norm(an_res.collect(['rel_vel'])[0], axis=1)
    print(_rel_vel)
    from flowtracks.graphics import pdf_graph
    pdf_graph(_rel_vel, 100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that we pulled out the 'rel_vel' analysis column, but we could just as easily pull out one of the trajectory columns, the AnalysedScene transparently knows where to look for the column you asked for.

    And that's pretty much all there is to it. Except there is more. Check out the docstrings in the code, or ask on the openptv googlegroup for more information on what can be done.
    """)
    return


if __name__ == "__main__":
    app.run()
