import pandas as pd
import numpy as np
import pyvista as pv


def _cell_bounds(points, bound_position=0.5):
    """
    Calculate coordinate cell boundaries.

    Parameters
    ----------
    points: numpy.ndarray
        One-dimensional array of uniformly spaced values of shape (M,).

    bound_position: bool, optional
        The desired position of the bounds relative to the position
        of the points.

    Returns
    -------
    bounds: numpy.ndarray
        Array of shape (M+1,)

    Examples
    --------
    >>> a = np.arange(-1, 2.5, 0.5)
    >>> a
    array([-1. , -0.5,  0. ,  0.5,  1. ,  1.5,  2. ])
    >>> _cell_bounds(a)
    array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25,  1.75,  2.25])

    """
    if points.ndim != 1:
        msg = 'Only 1D points are allowed.'
        raise ValueError(msg)
    diffs = np.diff(points)
    delta = diffs[0] * bound_position
    return np.concatenate([[points[0] - delta], points + delta])

def create_visual():
    # Seed random number generator for reproducible plots
    rng = np.random.default_rng(seed=0)

    # First, create some dummy data

    # Approximate radius of the Earth
    RADIUS = 6371.0

    # Longitudes and latitudes
    x = np.arange(0, 360, 5)
    y = np.arange(-90, 91, 10)
    y_polar = 90.0 - y  # grid_from_sph_coords() expects polar angle

    xx, yy = np.meshgrid(x, y)


    # x- and y-components of the wind vector
    u_vec = np.cos(np.radians(xx))  # zonal
    v_vec = np.sin(np.radians(yy))  # meridional

    # Scalar data
    scalar = u_vec**2 + v_vec**2

    # Create arrays of grid cell boundaries, which have shape of (x.shape[0] + 1)
    xx_bounds = _cell_bounds(x)
    yy_bounds = _cell_bounds(y_polar)
    # Vertical levels
    # in this case a single level slightly above the surface of a sphere
    levels = [RADIUS * 1.01]

    grid_scalar = pv.grid_from_sph_coords(xx_bounds, yy_bounds, levels)

    # And fill its cell arrays with the scalar data
    grid_scalar.cell_data['example'] = np.array(scalar).swapaxes(-2, -1).ravel('C')

    # Make a plot
    p = pv.Plotter()
    p.add_mesh(pv.Sphere(radius=RADIUS))
    p.add_mesh(grid_scalar, clim=[0.1, 2.0], opacity=0.5, cmap='plasma')
    p.show()




if __name__ == '__main__':
    create_visual()