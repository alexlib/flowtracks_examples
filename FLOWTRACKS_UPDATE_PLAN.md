# Update plan: flowtracks_examples → postptv v1.1.1+

Align the example notebooks with the updated `postptv` (a.k.a. `flowtracks`) library
after the SPEEDUP_PLAN optimisations (commits `6945ad0`–`d09e26a`).

## Steps

1. **Dependency alignment** — point `pyproject.toml` to the local `postptv` sibling.
2. **Canonical imports** — normalize `Scene` imports and remove stale API references.
3. **Per-notebook fixes** — fix broken cell ordering, undefined variables, and
   hard-coded paths in each notebook.
4. **Path normalisation** — ensure all data paths (`test_data`, `test_h5`)
   resolve from repo root, `notebooks/`, and `marimo run`.
5. **README + gallery** — replace `jupyter_notebooks` references, add sibling-dependency note.
6. **Validation tests** — add light import/smoke tests for deterministic workflows.
7. **Smoke-test every notebook** — confirm each imports without error and finds
   its data.
