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
    return Path, go, mo, np


@app.cell
def _(Path, mo, np):
    from flowtracks.io import trajectories_table
    from flowtracks.scene import Scene

    trajects_hdf = Path("./pyPTV_folder/trajectories.h5")
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
def _(go, np):
    def create_plotly_frame(t_current, window, norm_factor, scene_obj):
        """Generates Plotly traces for a specific time frame using flowtracks format."""
        active_traj_ids = set()
        traces = []

        start_t, end_t = scene_obj.frame_range()

        t_min = int(max(start_t, t_current - window))
        t_max = int(min(end_t, t_current + window))

        # Scan window using scene.frame_by_time
        for t in range(t_min, t_max + 1):
            try:
                f = scene_obj.frame_by_time(t)
                for tid in f.trajid():
                    if tid not in active_traj_ids:
                        active_traj_ids.add(tid)

                        traj = scene_obj.trajectory_by_id(tid)

                        # Calculate mean velocity
                        vel = traj.velocity()
                        mean_v = np.mean(np.linalg.norm(vel, axis=1)) if len(vel) > 0 else 0

                        color_val = min(1.0, max(0.0, mean_v / norm_factor))

                        # Get segment for this window
                        pos = traj.pos()
                        times = traj.time()

                        # Find indices where times are within [t_min, t_max]
                        mask = (times >= t_min) & (times <= t_max)
                        seg = pos[mask]

                        if len(seg) > 1:
                            traces.append(
                                go.Scatter3d(
                                    x=seg[:, 0],
                                    z=seg[:, 2],  # Swap Y/Z as per original notebook
                                    y=seg[:, 1],
                                    mode="lines",
                                    line=dict(
                                        color=f"rgb({int(255 * (1 - color_val))}, {int(255 * color_val)}, 150)",
                                        width=3,
                                    ),
                                    name=f"ID {tid}",
                                    showlegend=False,
                                )
                            )
            except Exception:
                continue

        return traces

    return (create_plotly_frame,)


@app.cell
def _(max_t, min_t, mo):
    # Create a slider that updates the plot
    plotly_slider = mo.ui.slider(
        min_t,
        max_t,
        value=min_t,
        label="Time Frame",
    )

    time_window = mo.ui.slider(20, 100, value=20, label="Time Window (Frames)")
    velocity_norm = mo.ui.number(
        0.001, 0.1, value=0.05, label="Velocity Normalization Factor"
    )
    return plotly_slider, time_window, velocity_norm


@app.cell
def _(create_plotly_frame, go, np, time_window, velocity_norm):
    def interactive_plot(t_current, scene_obj):
        frames = create_plotly_frame(
            t_current, time_window.value, velocity_norm.value, scene_obj
        )

        # --- Add the two circles at y=0 and y=3 with radius 3.5 ---
        theta = np.linspace(0, 2 * np.pi, 100)
        x_circle = 3.5 * np.cos(theta)
        z_circle = 3.5 * np.sin(theta)

        circle_y0 = go.Scatter3d(
            x=x_circle,
            y=np.full_like(theta, -2),  # y = 0
            z=z_circle,
            mode="lines",
            line=dict(color="black", width=5, dash="dash"),
            name="Circle y=0",
            showlegend=False,
            hoverinfo="skip"
        )

        circle_y3 = go.Scatter3d(
            x=x_circle,
            y=np.full_like(theta, 2), # y = 3
            z=z_circle,
            mode="lines",
            line=dict(color="black", width=5, dash="dash"),
            name="Circle y=3",
            showlegend=False,
            hoverinfo="skip"
        )

        # Append the circles to the animation frame
        frames.extend([circle_y0, circle_y3])
        # -----------------------------------------------------------

        fig = go.Figure(data=frames)

        fig.update_layout(
            scene=dict(
                xaxis=dict(range=[-3.5, 3.5], title="X"),
                yaxis=dict(range=[-3.5, 3.5], title="Y"),  
                zaxis=dict(range=[-3.5, 3.5], title="Z"),
                bgcolor="rgb(25, 0, 0)",
                camera=dict(
                    up=dict(x=0, y=1, z=0),     # Set Y-axis as vertical
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=0, y=0.5, z=-2)  # Eye is at negative z, so positive z points into the screen
                )
            ),
            paper_bgcolor="rgb(25, 0, 0)",
            font_color="white",
            margin=dict(l=0, r=0, b=0, t=0),
            height=600,
        )
        return fig

    return (interactive_plot,)


@app.cell
def _(interactive_plot, mo, plotly_slider, scene, time_window, velocity_norm):
    _fig = interactive_plot(plotly_slider.value, scene)
    mo.vstack([time_window, velocity_norm, plotly_slider, mo.ui.plotly(_fig)])
    return


@app.cell
def _():
    # # _____________________________________________________________________________
    # # 4. HIGH-RES VIDEO EXPORT (MATPLOTLIB)
    # # _____________________________________________________________________________

    # mo.md("### 🎬 Export High-Res Video (Matplotlib)")
    # mo.md("This generates an MP4 file. It may take a moment.")

    # export_button = mo.ui.button(
    #     label="Generate Video (MP4)", label_when_running="Generating..."
    # )

    # max_t = max(time_index.keys()) if time_index else 0

    # @export_button.on_click
    # def generate_video(_):
    #     import matplotlib

    #     matplotlib.use("Agg")  # Non-interactive backend for saving

    #     fig = plt.figure(figsize=(9, 7), facecolor=(0.1, 0.0, 0.0))
    #     ax = fig.add_subplot(projection="3d", facecolor=(0.1, 0.0, 0.0))

    #     # Axis styling
    #     ax.set_xlim(-40, 40)
    #     ax.set_ylim(-40, 40)
    #     ax.set_zlim(-40, 40)
    #     ax.grid(False)
    #     ax.set_xticks([])
    #     ax.set_yticks([])
    #     ax.set_zticks([])
    #     ax.xaxis.pane.fill = False
    #     ax.yaxis.pane.fill = False
    #     ax.zaxis.pane.fill = False
    #     ax.w_xaxis.line.set_color("w")
    #     ax.w_yaxis.line.set_color("w")
    #     ax.w_zaxis.line.set_color("w")

    #     cmap = plt.get_cmap("winter")
    #     frames_range = range(0, max_t, 2)  # Skip every other frame for speed

    #     def init():
    #         return []

    #     def update(frm):
    #         ax.clear()
    #         # Re-apply styles (matplotlib clears styles on clear)
    #         ax.set_facecolor((0.1, 0.0, 0.0))
    #         ax.set_xlim(-40, 40)
    #         ax.set_ylim(-40, 40)
    #         ax.set_zlim(-40, 40)
    #         ax.set_xticks([])
    #         ax.set_yticks([])
    #         ax.set_zticks([])
    #         ax.grid(False)

    #         # Use flowtracks trajectory format
    #         active_traj_ids = set()

    #         for t in range(
    #             max(0, frm - time_window.value), min(max_t, frm + time_window.value) + 1
    #         ):
    #             if t in time_index:
    #                 for tid, traj, frame_idx, mean_v in time_index[t]:
    #                     if tid not in active_traj_ids:
    #                         active_traj_ids.add(tid)
    #                         color = cmap(min(1.0, mean_v / velocity_norm.value))

    #                         # Get segment for this window
    #                         pos = traj.pos()
    #                         n_frames = len(pos)

    #                         start_idx = max(0, frm - time_window.value)
    #                         end_idx = min(n_frames, frm + time_window.value + 1)

    #                         if start_idx < end_idx and start_idx < n_frames:
    #                             seg = pos[start_idx:end_idx]

    #                             if len(seg) > 1:
    #                                 # Note axis swap: x, z, y
    #                                 ax.plot(
    #                                     seg[:, 0],
    #                                     seg[:, 2],
    #                                     seg[:, 1],
    #                                     color=color,
    #                                     linewidth=1.5,
    #                                 )
    #         return []

    #     ani = FuncAnimation(
    #         fig,
    #         update,
    #         frames=frames_range,
    #         init_func=init,
    #         blit=False,
    #         interval=50,
    #     )

    #     output_path = "trajectories_output.mp4"
    #     try:
    #         writer = FFMpegWriter(fps=30, metadata=dict(artist="Me"), bitrate=1800)
    #         ani.save(output_path, writer=writer)
    #         return mo.md(f"✅ **Video Saved:** `{output_path}`")
    #     except Exception as e:
    #         return mo.md(f"❌ **Error:** {str(e)}. Ensure ffmpeg is installed.")


    # export_button
    return


if __name__ == "__main__":
    app.run()
