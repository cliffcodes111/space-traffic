import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from satellite_list_object import satellite_database
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
###for the app
from flask import Flask, render_template
from io import BytesIO
import base64
from IPython.display import HTML

def run_app():
    app = Flask(__name__)
    #definining instance of class
    dataset = satellite_database(input_mode = "random_generated", number = 100, input_data = pd.DataFrame)

    def test_satellite_database(total_steps = 2, sat_object = dataset):
        object = sat_object
        object.build_input_data()
        total_df = pd.DataFrame()
        for time in range(1, total_steps):
            object.move_by_one_second()
            df = object.return_full_dataframe()
            total_df = pd.concat([total_df, df])
        return total_df
    for time_steps in range(1, 10):
        final_df = test_satellite_database()

        time_first = final_df.time.min()
        time_last = final_df.time.max()

        ###remove points that go too far out of the dataset
        final_df = final_df[final_df['coordinate_x']<10000]
        final_df = final_df[final_df['coordinate_y']<10000]
        final_df = final_df[final_df['coordinate_z']<10000]

        def update_graph(num):
            ax.cla()  # Clear the axes for each frame
            # Draw contour sphere with radius 6370 (wiremesh)
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = 6370 * np.outer(np.cos(u), np.sin(v))
            y = 6370 * np.outer(np.sin(u), np.sin(v))
            z = 6370 * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_wireframe(x, y, z, color='gray', linewidth=0.5, alpha=0.5)
            # Plot satellite positions at the current time step
            data_satellite = final_df[(final_df['time'] == (num + 1))&(final_df['classtype']=='fixed')]
            ax.scatter(data_satellite.coordinate_x, data_satellite.coordinate_y, data_satellite.coordinate_z, c='blue', marker = 'o')
            # Plot transport positions at the current time step
            data_transport = final_df[(final_df['time'] == (num + 1))&(final_df['classtype']=='transport')]
            ax.scatter(data_transport.coordinate_x, data_transport.coordinate_y, data_transport.coordinate_z, c='green', marker = '*')
            # Plot known junk positions at the current time step
            data_junk = final_df[(final_df['time'] == (num + 1))&(final_df['classtype']=='junk')]
            ax.scatter(data_junk.coordinate_x, data_junk.coordinate_y, data_junk.coordinate_z, c='red', marker = '^')
            ax.set_title(f'Space traffic control, time={num + 1}')
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

            # Save the satellite map to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            time.sleep(1)
            return ax, 
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ani = FuncAnimation(fig, update_graph, frames=2, interval=40, blit=False)
        final_fig = HTML(ani.to_jshtml())
        print(final_fig)
        return  f"<img src='data:image/png;base64,{final_fig}'/>"

if __name__ == "__main__":
    run_app()

