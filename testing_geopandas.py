import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

def test_geopandas():
    world_map_path = 'ne_110m_admin_0_countries.zip'
    world = gpd.read_file(world_map_path)
    ax = world.plot()
    ax.set_axis_off()
    plt.savefig('my_plot.png')

    return

if __name__ == '__main__':
    test_geopandas()