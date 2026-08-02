import marimo

__generated_with = "0.23.9"
app = marimo.App(width="wide")


@app.cell
def _():
    import marimo as mo
    import os
    import sys
    import subprocess
    from pathlib import Path

    return Path, mo, os, subprocess, sys


@app.cell
def _():
    NOTEBOOK_CATALOG = [
        # Data Loading & Zarr
        {
            "filename": "flowtracks_load_data_to_hdf_and_plot3d.py",
            "title": "Load Data & Export Zarr Store",
            "category": "Data Loading & Zarr",
            "icon": "📦",
            "description": "Load trajectories from text, HDF, or Zarr sources and export to cloud-native .zarr stores.",
            "tags": ["zarr", "hdf5", "io", "3d-plot"]
        },
        {
            "filename": "marimo_aorta_flowtracks.py",
            "title": "Aorta Flowtracks Zarr Pipeline",
            "category": "Data Loading & Zarr",
            "icon": "🫀",
            "description": "End-to-end 3D cardiac aortic flow processing driving smoothing and Eulerian binning from run.zarr.",
            "tags": ["aorta", "cardiac", "zarr", "smoothing", "eulerian"]
        },
        {
            "filename": "plotting_trajectories_using_postptv.py",
            "title": "Trajectories Auto-Detection",
            "category": "Data Loading & Zarr",
            "icon": "⚡",
            "description": "Transparently auto-detect and load Zarr stores, HDF5, or ptv_is text files.",
            "tags": ["auto-detect", "zarr", "postptv", "2d-projection"]
        },
        {
            "filename": "plotting_2d_trajectories_using_openptv_postptv.py",
            "title": "2D XY Trajectory Projection",
            "category": "Data Loading & Zarr",
            "icon": "📉",
            "description": "Read particle trajectories and render 2D XY spatial projections.",
            "tags": ["openptv", "postptv", "2d", "matplotlib"]
        },
        {
            "filename": "postptv_EX3915.py",
            "title": "PTVis & Kinematic Data Ingest",
            "category": "Data Loading & Zarr",
            "icon": "📊",
            "description": "Ingest PTVis trajectory files, compute velocity/acceleration arrays, and plot PDFs.",
            "tags": ["ptvis", "velocity", "acceleration", "histogram"]
        },
        {
            "filename": "read_alex_ruiz_data.py",
            "title": "Alex Ruiz Dataset Ingest",
            "category": "Data Loading & Zarr",
            "icon": "📁",
            "description": "Read v7.3 MAT files using hdf5storage and export Trajectory lists to Zarr.",
            "tags": ["matlab", "v7.3", "hdf5storage", "zarr"]
        },
        {
            "filename": "read_alex_ruiz_data-h5py.py",
            "title": "Alex Ruiz Dataset via h5py",
            "category": "Data Loading & Zarr",
            "icon": "🗄️",
            "description": "Read MATLAB datasets directly with h5py and convert to PyTables HDF5 & Zarr stores.",
            "tags": ["h5py", "matlab", "hdf5", "zarr"]
        },

        # Visualization
        {
            "filename": "marimo_zarr_dashboard.py",
            "title": "Zarr Cloud Store Dashboard",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🎛️",
            "description": "Interactive Zarr data dashboard inspecting chunked trajectory stores and velocity fields.",
            "tags": ["dashboard", "zarr", "cloud", "interactive"]
        },
        {
            "filename": "plotly_visualize_trajectories_nb.py",
            "title": "Interactive Plotly 3D Visualizer",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🎨",
            "description": "Interactive 3D trajectory visualizer with time window sliders and speed colormaps.",
            "tags": ["plotly", "3d", "interactive", "slider"]
        },
        {
            "filename": "plotly_3d_trajectories.py",
            "title": "Plotly 3D Trajectory Lines",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🌐",
            "description": "3D line plot of particle trajectories grouped by ID using Plotly Express.",
            "tags": ["plotly", "3d-line", "pandas"]
        },
        {
            "filename": "myptv_visualization.py",
            "title": "3D Colormapped Trajectories",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🌈",
            "description": "Render 3D trajectories with speed-dependent viridis colormapping.",
            "tags": ["myptv", "3d-plot", "colormap", "viridis"]
        },
        {
            "filename": "plot_frames.py",
            "title": "Multi-Panel Frame Plotting",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🎞️",
            "description": "Plot multi-panel 2D (x-y, y-z) and 3D frame snapshots.",
            "tags": ["frames", "2d-panels", "3d-view", "snapshots"]
        },
        {
            "filename": "animate_trajectories.py",
            "title": "3D Trajectory Video Animator",
            "category": "Visualization (2D/3D/Plotly)",
            "icon": "🎬",
            "description": "Generate high-resolution MP4 video animations of particle tails with camera controls.",
            "tags": ["animation", "mp4", "ffmpeg", "video"]
        },

        # Analysis & Scene Studies
        {
            "filename": "pair_analysis_example.py",
            "title": "Pairwise Trajectory Analysis",
            "category": "Analysis & Scene Studies",
            "icon": "👥",
            "description": "Pairwise particle trajectory analysis with velocity magnitude 3D scatter plots.",
            "tags": ["pairs", "scatter-3d", "dataframe"]
        },
        {
            "filename": "joint_pdf.py",
            "title": "Joint PDF & Conditional Stats",
            "category": "Analysis & Scene Studies",
            "icon": "📈",
            "description": "Compute joint probability density functions (PDF) of velocity vs acceleration.",
            "tags": ["pdf", "joint-pdf", "contour", "statistics"]
        },
        {
            "filename": "test_plot_pdf_subplots.py",
            "title": "Velocity PDF Subplots",
            "category": "Analysis & Scene Studies",
            "icon": "📐",
            "description": "Fit Gaussian distributions to particle velocity components and plot subplots.",
            "tags": ["pdf-fit", "gaussian", "subplots"]
        },
        {
            "filename": "hdf5_scene_analysis.py",
            "title": "DualScene & Particle Analysis",
            "category": "Analysis & Scene Studies",
            "icon": "🔬",
            "description": "Explore tracer and particle scenes iterating by frame, segment, and trajectory.",
            "tags": ["scene", "dualscene", "tracers", "analysis"]
        },
        {
            "filename": "linking_trajectories.py",
            "title": "Predictive Trajectory Linking",
            "category": "Analysis & Scene Studies",
            "icon": "🔗",
            "description": "Bridge broken trajectory gaps using predictive kinematic velocity matching.",
            "tags": ["linking", "gap-bridging", "kinematics"]
        },
        {
            "filename": "repeated_interpolation.py",
            "title": "Repeated Spatial Interpolation",
            "category": "Analysis & Scene Studies",
            "icon": "🔄",
            "description": "Evaluate local velocity interpolation consistency via random subsampling.",
            "tags": ["interpolation", "idw", "subsampling", "consistency"]
        }
    ]
    return (NOTEBOOK_CATALOG,)


@app.cell
def _(NOTEBOOK_CATALOG, mo):
    categories = ["All"] + sorted(list(set(item["category"] for item in NOTEBOOK_CATALOG)))
    
    search_bar = mo.ui.text(
        placeholder="Filter by title, tag, or keyword...",
        label="🔍 Search Notebooks",
        full_width=True
    )

    category_filter = mo.ui.dropdown(
        options=categories,
        value="All",
        label="📂 Filter by Category"
    )

    mo.vstack([
        mo.md("""
        # 🌊 Flowtracks Marimo Gallery & Library Index
        *An interactive library of 3D Particle Tracking Velocimetry (3D-PTV) notebooks, featuring cloud-native **Zarr** stores, HDF5, Plotly, and marimo reactive workflows.*
        """),
        mo.hstack([category_filter, search_bar], gap=2)
    ])
    return category_filter, search_bar


@app.cell
def _(NOTEBOOK_CATALOG, category_filter, search_bar):
    query = search_bar.value.lower().strip()
    cat = category_filter.value

    filtered = []
    for item in NOTEBOOK_CATALOG:
        if cat != "All" and item["category"] != cat:
            continue
        if query:
            match_title = query in item["title"].lower()
            match_file = query in item["filename"].lower()
            match_desc = query in item["description"].lower()
            match_tags = any(query in t.lower() for t in item["tags"])
            if not (match_title or match_file or match_desc or match_tags):
                continue
        filtered.append(item)
    return (filtered,)


@app.cell
def _(filtered, NOTEBOOK_CATALOG, mo, os, subprocess, sys):
    def _launch(filename):
        path = os.path.join("notebooks", filename)
        subprocess.Popen([sys.executable, "-m", "marimo", "edit", path])

    cards = []
    for nb in filtered:
        tags_html = " ".join([f"`#{tag}`" for tag in nb["tags"]])
        cmd_code = f"uv run marimo edit notebooks/{nb['filename']}"
        
        btn = mo.ui.button(
            label=f"🚀 Launch {nb['filename']}",
            on_change=lambda _, fn=nb["filename"]: _launch(fn)
        )

        card_md = mo.md(f"""
        ### {nb['icon']} {nb['title']}
        **Category:** `{nb['category']}`  
        **File:** [`{nb['filename']}`](file:///C:/Users/alex/projects/flowtracks_examples/notebooks/{nb['filename']})  
        {nb['description']}  

        **Tags:** {tags_html}  
        **Terminal Run:** `{cmd_code}`
        """)

        cards.append(mo.vstack([card_md, btn], gap=1))

    stats_msg = f"Showing **{len(filtered)}** of **{len(NOTEBOOK_CATALOG)}** notebooks in library gallery"

    gallery_view = mo.vstack([
        mo.md(stats_msg),
        mo.md("---"),
        mo.vstack(cards, gap=2) if cards else mo.md("*No notebooks match your search query.*")
    ])

    gallery_view
    return


if __name__ == "__main__":
    app.run()
