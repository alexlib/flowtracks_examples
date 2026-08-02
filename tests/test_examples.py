"""
Lightweight smoke tests for the flowtracks_examples deterministic workflows.

These tests exercise text-based trajectory loading, HDF5 round-trips, and
Scene iteration without opening any GUI windows.  Matplotlib and Plotly
rendering are not invoked.
"""

import os, sys, tempfile, pathlib

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
TEST_DATA = REPO / "test_data"
TEST_H5 = REPO / "test_h5"


# ── Fixtures ────────────────────────────────────────────────────────────────


def _ptv_is_files_exist():
    return (TEST_DATA / "ptv_is.101000").exists()


def _h5_files_exist():
    return (TEST_H5 / "traj_GT.h5").exists()


def _zarr_files_exist():
    return (REPO / "test_zarr" / "trajectories.zarr").exists()



# ── Text-ingest tests ───────────────────────────────────────────────────────


@pytest.mark.skipif(not _ptv_is_files_exist(), reason="test_data/ not found")
class TestTextIngest:
    def test_iter_trajectories_ptvis(self):
        from flowtracks.io import iter_trajectories_ptvis

        template = str(TEST_DATA / "ptv_is.%d")
        trjs = list(iter_trajectories_ptvis(template, first=101000, last=101020))
        assert len(trjs) > 0, "expected at least one trajectory"

    def test_trajectories_ptvis(self):
        from flowtracks.io import trajectories_ptvis

        template = str(TEST_DATA / "ptv_is.%d")
        trjs = trajectories_ptvis(template, traj_min_len=3)
        assert len(trjs) > 0

    def test_min_length_filter(self):
        from flowtracks.io import iter_trajectories_ptvis

        template = str(TEST_DATA / "ptv_is.%d")
        all_trjs = list(iter_trajectories_ptvis(template, first=101000, last=101020))
        long_trjs = list(
            iter_trajectories_ptvis(template, first=101000, last=101020, traj_min_len=10)
        )
        assert len(long_trjs) <= len(all_trjs)

    def test_pos_vel_shapes(self):
        from flowtracks.io import iter_trajectories_ptvis

        template = str(TEST_DATA / "ptv_is.%d")
        trjs = list(iter_trajectories_ptvis(template, first=101000, last=101005))
        for tr in trjs:
            p = tr.pos()
            v = tr.velocity()
            assert p.ndim == 2 and p.shape[1] == 3
            assert v.shape == p.shape

    def test_pandas_dataframe(self):
        import pandas as pd
        from flowtracks.io import iter_trajectories_ptvis

        template = str(TEST_DATA / "ptv_is.%d")
        trjs = list(iter_trajectories_ptvis(template, first=101000, last=101010))
        rows = []
        for tr in trjs:
            p = tr.pos()
            v = tr.velocity()
            for i in range(p.shape[0]):
                rows.append(
                    {"trajid": tr.trajid(), "x": p[i, 0], "y": p[i, 1], "z": p[i, 2],
                     "u": v[i, 0], "v": v[i, 1], "w": v[i, 2]}
                )
        df = pd.DataFrame(rows)
        assert not df.empty
        assert all(c in df.columns for c in ["x", "y", "z", "u", "v", "w"])


# ── HDF5 round-trip tests ───────────────────────────────────────────────────


@pytest.mark.skipif(not _ptv_is_files_exist(), reason="test_data/ not found")
class TestHdfRoundTrip:
    @pytest.fixture
    def temp_h5(self):
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as f:
            fname = f.name
        yield fname
        os.unlink(fname)

    def test_save_and_reload(self, temp_h5):
        from flowtracks.io import trajectories_ptvis, save_particles_table, trajectories_table

        template = str(TEST_DATA / "ptv_is.%d")
        original = trajectories_ptvis(template, traj_min_len=3)
        save_particles_table(temp_h5, original)
        reloaded = trajectories_table(temp_h5)
        assert len(reloaded) == len(original)
        by_id = {tr.trajid(): tr for tr in original}
        for r in reloaded:
            o = by_id.get(r.trajid())
            assert o is not None, f"trajid {r.trajid()} missing from original"
            np.testing.assert_array_almost_equal(o.pos(), r.pos())

    def test_save_and_scene(self, temp_h5):
        from flowtracks.io import trajectories_ptvis, save_particles_table
        from flowtracks.scene import Scene

        template = str(TEST_DATA / "ptv_is.%d")
        original = trajectories_ptvis(template, traj_min_len=3)
        save_particles_table(temp_h5, original)

        scene = Scene(temp_h5)
        trjs = list(scene.iter_trajectories())
        assert len(trjs) == len(original)


# ── Scene tests (pre-built HDF5) ────────────────────────────────────────────


@pytest.mark.skipif(not _h5_files_exist(), reason="test_h5/ not found")
class TestSceneH5:
    @pytest.fixture
    def scene_gt(self):
        from flowtracks.scene import Scene
        return Scene(str(TEST_H5 / "traj_GT.h5"))

    def test_iter_trajectories(self, scene_gt):
        trjs = list(scene_gt.iter_trajectories())
        assert len(trjs) > 0

    def test_iter_frames(self, scene_gt):
        frames = list(scene_gt.iter_frames())
        assert len(frames) > 0

    def test_trajectory_by_id(self, scene_gt):
        ids = scene_gt.trajectory_ids()
        assert len(ids) > 0
        tr = scene_gt.trajectory_by_id(ids[0])
        assert tr.trajid() == ids[0]

    def test_keys(self, scene_gt):
        keys = scene_gt.keys()
        assert "pos" in keys
        assert "velocity" in keys

    def test_dual_scene(self):
        from flowtracks.scene import DualScene
        from flowtracks.particle import Particle

        part = Particle(1e-4, 1.0)
        ds = DualScene(
            str(TEST_H5 / "traj_GT.h5"),
            str(TEST_H5 / "traj_RC.h5"),
            frate=1.0,
            particle=part,
        )
        frames = list(ds.iter_frames())
        assert len(frames) > 0
        for f in frames:
            assert hasattr(f, "tracers")
            assert hasattr(f, "particles")


# ── Interpolation tests (no data files needed) ──────────────────────────────


class TestInterpolation:
    def test_idw_call(self):
        from flowtracks.interpolation import InverseDistanceWeighter

        rng = np.random.default_rng(42)
        n, m, d = 50, 10, 3
        tracer_pos = rng.random((n, 3))
        interp_points = rng.random((m, 3))
        data = rng.random((n, d))

        w = InverseDistanceWeighter(num_neighbs=4)
        result = w(tracer_pos, interp_points, data)
        assert result.shape == (m, d)
        assert np.all(np.isfinite(result))

    def test_rbf_call(self):
        from flowtracks.interpolation import Interpolant

        rng = np.random.default_rng(42)
        n, m, d = 50, 10, 3
        tracer_pos = rng.random((n, 3))
        interp_points = rng.random((m, 3))
        data = rng.random((n, d))

        rbf = Interpolant("rbf", num_neighbs=4, param=1e5)
        result = rbf(tracer_pos, interp_points, data)
        assert result.shape == (m, d)
        assert np.all(np.isfinite(result))


# ── Zarr ingest & round-trip tests ─────────────────────────────────────────


@pytest.mark.skipif(not _zarr_files_exist(), reason="test_zarr/ not found")
class TestZarrIngest:
    def test_read_zarr_trajectories(self):
        from flowtracks.io import read_zarr_trajectories

        zarr_path = REPO / "test_zarr" / "trajectories.zarr"
        trjs = read_zarr_trajectories(zarr_path)
        assert len(trjs) > 0, "expected at least one trajectory in Zarr store"

    def test_trajectories_auto_detect_zarr(self):
        from flowtracks.io import trajectories

        zarr_path = str(REPO / "test_zarr" / "trajectories.zarr")
        trjs = trajectories(zarr_path)
        assert len(trjs) > 0

    def test_zarr_pos_vel_shapes(self):
        from flowtracks.io import read_zarr_trajectories

        zarr_path = REPO / "test_zarr" / "trajectories.zarr"
        trjs = read_zarr_trajectories(zarr_path)
        for tr in trjs[:10]:
            p = tr.pos()
            assert p.ndim == 2 and p.shape[1] == 3


@pytest.mark.skipif(not _ptv_is_files_exist(), reason="test_data/ not found")
class TestZarrRoundTrip:
    def test_save_and_reload_zarr(self, tmp_path):
        from flowtracks.io import (
            trajectories_ptvis,
            save_zarr_trajectories,
            read_zarr_trajectories,
            trajectories,
        )

        template = str(TEST_DATA / "ptv_is.%d")
        original = trajectories_ptvis(template, traj_min_len=3)
        temp_zarr = tmp_path / "sample.zarr"
        save_zarr_trajectories(original, temp_zarr)

        reloaded = read_zarr_trajectories(temp_zarr)
        assert len(reloaded) == len(original)

        reloaded_auto = trajectories(str(temp_zarr))
        assert len(reloaded_auto) == len(original)

        by_id = {tr.trajid(): tr for tr in original}
        for r in reloaded:
            o = by_id.get(r.trajid())
            assert o is not None
            np.testing.assert_array_almost_equal(o.pos(), r.pos())


# ── Marimo notebook smoke tests ─────────────────────────────────────────────


class TestMarimoNotebooksImports:
    def test_all_notebooks_syntax_and_app(self):
        import ast

        nb_dir = REPO / "notebooks"
        nb_files = list(nb_dir.glob("*.py"))
        assert len(nb_files) == 19, f"expected 19 notebook files, found {len(nb_files)}"


        for nb_path in nb_files:
            code = nb_path.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=str(nb_path))
            has_app = any(
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "app" for target in node.targets)
                for node in tree.body
            )
            assert has_app, f"{nb_path.name} missing 'app = marimo.App(...)' definition"



