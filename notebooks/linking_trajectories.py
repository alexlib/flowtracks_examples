import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    # -*- coding: utf-8 -*-
    """
    Problem: the candidate may already be linked. Need to register the candidate 
    and update both if the candidate has a better link.
    Created on Wed Feb 22 12:08:02 2017
    @author: yosef, based on attempt by lillyverso
    """

    import itertools as it, numpy as np
    import matplotlib.pyplot as plt
    # '%matplotlib tk' command supported automatically in marimo

    from flowtracks.scene import Scene
    from flowtracks.trajectory import Trajectory

    return Scene, Trajectory, it, np, plt


@app.cell
def _(Scene):
    from pathlib import Path
    base_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    h5_path = base_dir / 'test_h5' / 'traj_GT.h5' if (base_dir / 'test_h5').exists() else base_dir / '..' / 'test_h5' / 'traj_GT.h5'
    frate = 100
    scn = Scene(str(h5_path))
    return frate, scn



@app.cell
def _():
    distThresh = 0.0025;   
    maxDt = 1;
    minLength = 25;       # length of elemnts in the trajs
    return distThresh, maxDt, minLength


@app.cell
def _(minLength, scn):
    # Though this won't be necessary if you don't save the short ones at all in the
    # HDF conversion.
    long_trajects = list(filter(
        lambda trj: len(trj) > minLength, scn.iter_trajectories()))
    return (long_trajects,)


@app.cell
def _(distThresh, frate, it, long_trajects, maxDt, np):
    # Keyed by trajid, value is a tuple (id, dist) where id is the best candidate 
    # trajectory for linking, and dist is the average-distance measure for this
    # pair (the measure to beat)
    links = {}
    back_links = {}
    for _trj1, _trj2 in it.combinations(long_trajects, 2):
        dt = (_trj2.time(0) - _trj1.time(-1)) / frate
        if not 0 < dt <= maxDt:
            continue
        master_id = _trj1.trajid()
        slave_id = _trj2.trajid()
        links.setdefault(master_id, (None, distThresh))  # print(trj1, trj2, dt)
        back_links.setdefault(slave_id, (None, distThresh))
        min_dist = min(links[master_id][1], back_links[slave_id][1])
        predicted_forward = _trj1.pos(-1) + dt * _trj1.velocity(-1)
        predicted_backward = _trj2.pos(0) - dt * _trj2.velocity(0)
        dist_forward = np.linalg.norm(predicted_forward - _trj2.pos(0))
        dist_backward = np.linalg.norm(predicted_backward - _trj1.pos(-1))
        avg_dist = (dist_forward + dist_backward) / 2.0
        if avg_dist < min_dist:  # Continue trj1 forward one time interval, and trj2 backward one interval.
            old_link = back_links[slave_id][0]  # If the evarage distance between each predicted point and the other traj's
            if old_link is not None:  # endpoint meets the criteria - connect.
                links[old_link] = (None, distThresh)
            links[master_id] = (slave_id, avg_dist)
            back_links[slave_id] = (master_id, avg_dist)
    print(f'candidates: {links}')  # Possible register candidate:
    return (links,)


@app.cell
def _(Trajectory, links, np, scn):
    # Weld the final best candidates.
    out_trajects = []
    used_trids = set()  # don't repeat taken candidates as masters.
    for trid, cand in links.items():
        if trid in used_trids:
            continue
        trj_weld = scn.trajectory_by_id(trid)
        while cand[0] is not None:
            used_trids.add(cand[0])
            _trj1 = trj_weld
            _trj2 = scn.trajectory_by_id(cand[0])
            trj_weld = Trajectory(np.vstack((_trj1.pos(), _trj2.pos())), np.vstack((_trj1.velocity(), _trj2.velocity())), trajid=_trj1.trajid(), time=np.hstack((_trj1.time(), _trj2.time())), accel=np.vstack((_trj1.accel(), _trj2.accel())))
            if cand[0] not in links:
                break
            cand = links[cand[0]]
        out_trajects.append(trj_weld)
    return (out_trajects,)


@app.cell
def _(long_trajects, out_trajects, plt):
    # Check wheter we link correctly the trajs
    # plot the trajs
    # Check wheter we link correctly the trajs
    # plot the trajs
    fig = plt.figure(figsize=(7,7))
    for trj in long_trajects:
        pos = trj.pos()
        plt.plot(pos[:,0], pos[:,1],'-')

    # plt.show()

    # fig = plt.figure(figsize=(7,7))
    for trj in out_trajects:
        pos = trj.pos()
        plt.plot(pos[:,0], pos[:,1],'--')

    plt.show()
    return


if __name__ == "__main__":
    app.run()
