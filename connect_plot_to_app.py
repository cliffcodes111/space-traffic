
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from satellite_list_object import satellite_database
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from io import BytesIO
import base64


def run_app(frame=1, total_frames=24):
    try:
        dataset = satellite_database(input_mode = "random_generated", number = 100, input_data = pd.DataFrame)
    except Exception as e:
        return f"<div style='color:red;'>Error initializing satellite database: {e}</div>", total_frames

    def test_satellite_database(total_steps = total_frames, sat_object = dataset):
        object = sat_object
        object.build_input_data()
        total_df = pd.DataFrame()
        for t in range(1, total_steps):
            object.move_by_one_second()
            df = object.return_full_dataframe()
            total_df = pd.concat([total_df, df])
        return total_df

    try:
        final_df = test_satellite_database()
        final_df = final_df[final_df['coordinate_x']<10000]
        final_df = final_df[final_df['coordinate_y']<10000]
        final_df = final_df[final_df['coordinate_z']<10000]

        fig = plt.figure(facecolor='#23272a')
        ax = fig.add_subplot(111, projection='3d', facecolor='#23272a')

        # Draw contour sphere with radius 6370 (wiremesh)
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = 6370 * np.outer(np.cos(u), np.sin(v))
        y = 6370 * np.outer(np.sin(u), np.sin(v))
        z = 6370 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z, color='black', linewidth=0.5, alpha=0.5)
        fig.patch.set_facecolor('#23272a')
        ax.set_facecolor('#23272a')

        # Plot satellite positions at the current time step
        data_satellite = final_df[(final_df['time'] == (frame))&(final_df['classtype']=='fixed')]
        ax.scatter(data_satellite.coordinate_x, data_satellite.coordinate_y, data_satellite.coordinate_z, c='blue', marker = 'o')
        # Plot transport positions at the current time step
        data_transport = final_df[(final_df['time'] == (frame))&(final_df['classtype']=='transport')]
        ax.scatter(data_transport.coordinate_x, data_transport.coordinate_y, data_transport.coordinate_z, c='green', marker = '*')
        # Plot known junk positions at the current time step
        data_junk = final_df[(final_df['time'] == (frame))&(final_df['classtype']=='junk')]
        ax.scatter(data_junk.coordinate_x, data_junk.coordinate_y, data_junk.coordinate_z, c='red', marker = '^')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.grid(True)
        ax.set_xlim([-10000, 10000])
        ax.set_ylim([-10000, 10000])
        ax.set_zlim([-10000, 10000])

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        plt.close(fig)
        return f"<img src='data:image/png;base64,{data}'/>", total_frames
    except Exception as e:
        return f"<div style='color:red;'>Error generating plot: {e}</div>", total_frames

