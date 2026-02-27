import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from matplotlib.animation import FuncAnimation, FFMpegWriter
    from concurrent.futures import ProcessPoolExecutor
    from pathlib import Path
    import warnings

    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore")
    return FFMpegWriter, FuncAnimation, Path, mo, np, plt


@app.cell
def _(Path, mo, np):
    from flowtracks.io import trajectories_table
    from flowtracks.scene import Scene

    trajects_hdf = Path("./test_h5/test.h5")
    scene = Scene(trajects_hdf)

    min_t, max_t = scene.frame_range()

    # The flowtracks.scene.Scene object automatically manages time-indexed data
    # (e.g., via scene.iter_frames() or scene.frame_range()), so we don't need 
    # to build and maintain a manual time_index.

    # We only need to compute the overall mean velocity for our summary.
    _all_speeds = []

    for traj in scene.iter_trajectories():
        vel = traj.velocity()
        if len(vel) > 0:
            _all_speeds.append(np.linalg.norm(vel, axis=1))

    if _all_speeds:
        mean_v = np.mean(np.concatenate(_all_speeds))
    else:
        mean_v = 0.0

    mo.md(f"✅ **Loaded:** {len(scene.trajectory_ids())} valid trajectories. Mean velocity {mean_v:.2f} a.u. Frame range: {min_t} to {max_t}.")
    return max_t, min_t, scene


@app.cell
def _(max_t, min_t, mo):
    time_window = mo.ui.slider(1, 100, value=5, label="Time Window (Frames)")
    velocity_norm = mo.ui.number(
        0.001, 0.1, value=0.05, label="Velocity Normalization Factor"
    )
    frame_range_slider = mo.ui.range_slider(
        min_t, max_t, value=[min_t, max_t], label="Video Frame Range"
    )
    mo.vstack([
        mo.md("#### Video Configuration"),
        time_window, 
        velocity_norm,
        frame_range_slider
    ])
    return frame_range_slider, time_window, velocity_norm


@app.cell
def _(
    FFMpegWriter,
    FuncAnimation,
    frame_range_slider,
    mo,
    np,
    plt,
    scene,
    time_window,
    velocity_norm,
):
    # _____________________________________________________________________________
    # 4. HIGH-RES VIDEO EXPORT (MATPLOTLIB)
    # _____________________________________________________________________________

    mo.md("### 🎬 Export High-Res Video (Matplotlib)\nThis generates an MP4 file. It may take a moment.")

    export_button = mo.ui.run_button(
        label="Generate Video (MP4)"
    )

    def generate_video():
        import matplotlib

        matplotlib.use("Agg")  # Non-interactive backend for saving

        fig = plt.figure(figsize=(9, 7), facecolor=(0.1, 0.0, 0.0))
        ax = fig.add_subplot(projection="3d", facecolor=(0.1, 0.0, 0.0))

        # Axis styling
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_zlim(-3.5, 3.5)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Configure camera view
        # In matplotlib, X horizontal, Y depth, Z vertical.
        # To have X right, Z depth, Y up we can use azim=-90, elev=0.
        ax.view_init(elev=10, azim=-90)

        cmap = plt.get_cmap("viridis")

        # Use the selected range from the frame slider!
        start_frame, end_frame = frame_range_slider.value
        frames_range = range(start_frame, end_frame + 1, 2)  # Skip every other frame for speed

        def init():
            return []

        def update(frm):
            ax.clear()
            # Re-apply styles
            ax.set_facecolor((0.1, 0.0, 0.0))
            ax.set_xlim(-3.5, 3.5)
            ax.set_ylim(-3.5, 3.5)
            ax.set_zlim(-3.5, 3.5)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            ax.grid(False)
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False

            # Draw the two circles at y=0 and y=3 (mapping to plt Z=0, Z=3)
            theta = np.linspace(0, 2 * np.pi, 100)
            x_circle = 3.5 * np.cos(theta)
            z_circle = 3.5 * np.sin(theta)
            # We plot X=x, Y=z, Z=y
            ax.plot(x_circle, z_circle, np.zeros_like(theta), color="black", linestyle="--", linewidth=2)
            ax.plot(x_circle, z_circle, np.full_like(theta, 3), color="black", linestyle="--", linewidth=2)

            active_traj_ids = set()

            try:
                # We want to show trajectories up to current frame with tail of time_window
                f = scene.frame_by_time(frm)
                for tid in f.trajid():
                    active_traj_ids.add(tid)
                    traj = scene.trajectory_by_id(tid)

                    # Get mean velocity for color mapping
                    vel = traj.velocity()
                    mean_v = np.mean(np.linalg.norm(vel, axis=1)) if len(vel) > 0 else 0
                    color_val = min(1.0, max(0.0, mean_v / velocity_norm.value))
                    color = cmap(color_val)

                    # Get segment for this window
                    pos = traj.pos()
                    times = traj.time()

                    t_start = frm - time_window.value
                    t_end = frm

                    mask = (times >= t_start) & (times <= t_end)
                    seg = pos[mask]

                    if len(seg) > 0:
                        # Draw tail
                        if len(seg) > 1:
                            # mapping to Matplotlib 3D axes (X=x, Y=z, Z=y)
                            ax.plot(
                                seg[:, 0],
                                seg[:, 2],
                                seg[:, 1],
                                color=color,
                                linewidth=1.5,
                            )

                        # Draw moving dot at the head (last frame in the segment)
                        head = seg[-1]
                        ax.scatter(
                            head[0],
                            head[2],
                            head[1],
                            color=color,
                            s=20,  # Dot size
                        )
            except Exception:
                pass

            return []

        ani = FuncAnimation(
            fig,
            update,
            frames=frames_range,
            init_func=init,
            blit=False,
            interval=50,
        )

        output_path = f"trajectories_output_{start_frame}_to_{end_frame}.mp4"
        try:
            writer = FFMpegWriter(fps=30, metadata=dict(artist="Me"), bitrate=1800)
            ani.save(output_path, writer=writer)
            return mo.md(f"✅ **Video Saved:** `{output_path}`")
        except Exception as e:
            return mo.md(f"❌ **Error:** {str(e)}. Ensure ffmpeg is installed.")


    return export_button, generate_video


@app.cell
def _(export_button, generate_video, mo):
    mo.vstack([
        export_button,
        generate_video() if export_button.value else mo.md("")
    ])
    return


if __name__ == "__main__":
    app.run()
