# Update plan: flowtracks_examples → postptv v1.2.0+ (Zarr Enabled)

Align the example notebooks with the updated `postptv` (a.k.a. `flowtracks`) library
after the SPEEDUP_PLAN optimisations and unified Zarr architecture integration.

## Steps

1. **Dependency alignment** — point `pyproject.toml` to local `postptv` (`flowtracks = { path = "../postptv", editable = true }`) and `zarr>=3.0.0`. [Completed]
2. **Canonical imports & Zarr API** — update notebooks to use `read_zarr_trajectories`, `save_zarr_trajectories`, and auto-detecting `trajectories()` for `.zarr` stores. [Completed]
3. **Per-notebook fixes** — update data loading in example notebooks (`flowtracks_load_data_to_hdf_and_plot3d.py`, `plotting_trajectories_using_postptv.py`, `plotting_2d_trajectories_using_openptv_postptv.py`, `postptv_EX3915.py`, `plotly_3d_trajectories.py`, `read_alex_ruiz_data.py`, `read_alex_ruiz_data-h5py.py`). [Completed]
4. **Path & Store normalisation** — add `test_zarr` dataset (`test_zarr/trajectories.zarr`) and ensure all data paths resolve cleanly from repo root, `notebooks/`, and `marimo run`. [Completed]
5. **README & Gallery update** — document Zarr store workflows and updated gallery. [Completed]
6. **Validation tests** — add Zarr ingest (`TestZarrIngest`) and Zarr round-trip (`TestZarrRoundTrip`) pytest tests in `tests/test_examples.py`. [Completed]
7. **Smoke-test every notebook & test suite** — all 18 pytest unit tests pass cleanly. [Completed]

