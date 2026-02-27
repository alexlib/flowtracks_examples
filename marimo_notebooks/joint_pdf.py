import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Following Yosef Meller Ph.D. work
    """)
    return


@app.cell
def _():
    """
    Created on Wed Jun 29 14:19:49 2016

    @author: yosef meller
    """

    import numpy as np, matplotlib.pyplot as pl
    from flowtracks.graphics import pdf_bins, generalized_histogram_disp
    from itertools import cycle

    return np, pl


@app.cell
def _(np, pl):
    def joint_pdf(val1, val2, log=False, cmap=None, **kwds):
        """
        Generate a contour-map showing the joint-pdf of two forces f1 and f2.
        Underlying the map is a color-map of average coloring value for each bin.

        Arguments:
        val1, val2 - equal-length arrays with the data for the contour axes x
            and y respectively.
        log - plot the log10 of the histogram rather than the raw histogram.
        cmap - if a matplotlib colormap, show a color map instead of a contour map.
            default is None (contour map).
        kwds - passed on to MAtplotlib underlying function.
        """
        num_bins = 100
        hist, xedges, yedges = np.histogram2d(
            val1, val2, bins=num_bins, density=True
        )

        if log:
            hist = np.log10(hist)

        xs = np.mean([xedges[:-1], xedges[1:]], axis=0)
        ys = np.mean([yedges[:-1], yedges[1:]], axis=0)

        if not cmap:
            cs = pl.contour(xs, ys, hist.T, 10, colors="k", origin="lower")
            pl.clabel(cs)
        else:
            pl.imshow(
                hist.T,
                aspect="auto",
                origin="lower",
                cmap=cmap,
                extent=(val1.min(), val1.max(), val2.min(), val2.max()),
                **kwds,
            )
            pl.colorbar()

        pl.show()

    return (joint_pdf,)


@app.cell
def _():
    from flowtracks.io import Scene

    particles = Scene("../test_h5/traj_GT.h5")
    return (particles,)


@app.cell
def _(particles):
    traj = list(particles.iter_trajectories())
    return


@app.cell
def _(np, particles):
    vel = np.hstack(
        [
            np.sum(tr.velocity() ** 2, axis=1)
            for tr in particles.iter_trajectories()
        ]
    )
    acc = np.hstack(
        [np.sum(tr.accel() ** 2, axis=1) for tr in particles.iter_trajectories()]
    )
    return acc, vel


@app.cell
def _(acc, np, vel):
    p = np.percentile(vel, [5, 95])
    vel_1 = vel[np.logical_and(vel > p[0], vel < p[1])]
    p = np.percentile(acc, [5, 95])
    acc_1 = acc[np.logical_and(acc > p[0], acc < p[1])]
    return acc_1, vel_1


@app.cell
def _(acc_1, joint_pdf, np, pl, vel_1):
    joint_pdf(vel_1, np.sqrt(acc_1), log=True, cmap=pl.cm.viridis)
    return


@app.cell
def _(np, pl):
    def conditional_stats_graph(series, condition, num_bins):
        """
        Graph the means and standard deviations of a series as a function of the
        condition.

        Arguments:
        series - a set of measurements, 1D array.
        condition - the corresponding value of the condition in each measurement.
        num_bins - number of bins to make for the conditional.
        """
        bin_edges = np.linspace(condition.min(), condition.max(), num_bins + 1)
        counts = np.empty(num_bins)
        means = np.empty(num_bins)
        stds = np.empty(num_bins)
        for hbin in range(num_bins):
            in_bin = (condition >= bin_edges[hbin]) & (
                condition < bin_edges[hbin + 1]
            )
            bin_vals = series[in_bin]
            counts[hbin] = len(bin_vals)
            means[hbin] = bin_vals.mean()
            stds[hbin] = bin_vals.std()
        # print(f"counts = {counts}, \n means = {means},\n stds = {stds}")
        bin_halfwidth = 0.5 * (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[:-1] + bin_halfwidth
        means[counts < 30] = np.nan
        pl.plot(
            bin_centers, stds
        )  # Not enough data  #pl.errorbar(means, bin_centers, xerr=stds)from mixintel.graphs import conditional_stats_graph

    return (conditional_stats_graph,)


@app.cell
def _(conditional_stats_graph, particles, pl):
    # or using some helper functions:
    # .collect
    acc_2, vel_2 = particles.collect(["accel", "velocity"])
    num_bins = 20
    conditional_stats_graph(acc_2[:, 0], vel_2[:, 0], num_bins)
    conditional_stats_graph(acc_2[:, 1], vel_2[:, 1], num_bins)
    conditional_stats_graph(acc_2[:, 2], vel_2[:, 2], num_bins)
    pl.legend(("$a_x(u)$", "$a_y(v)$", "$a_z(w)$"))
    pl.xlabel("Velocity")
    pl.ylabel("Conditional acceleration")
    pl.show()
    return


if __name__ == "__main__":
    app.run()
