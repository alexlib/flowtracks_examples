import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import os
    import sys
    import subprocess

    return mo, os, subprocess, sys


@app.cell
def _(mo, os, subprocess, sys):
    _notebook_dir = "notebooks"
    _notebook_files = sorted([f for f in os.listdir(_notebook_dir) if f.endswith(".py")]) if os.path.exists(_notebook_dir) else []

    def _open_nb(path):
        # Launch marimo edit in a new background process so it doesn't block this notebook
        subprocess.Popen([sys.executable, "-m", "marimo", "edit", path])

    _buttons = [
        mo.ui.button(
            label=f"🚀 Open {nb}",
            on_change=lambda _, p=os.path.join(_notebook_dir, nb): _open_nb(p)
        )
        for nb in _notebook_files
    ]

    mo.md(f"""
    # 📚 Notebook Gallery

    Click on a notebook below to open it in a new window:

    {mo.vstack(_buttons) if _buttons else f"*No notebooks found in the `{_notebook_dir}` folder.*"}
    """)
    return


if __name__ == "__main__":
    app.run()
