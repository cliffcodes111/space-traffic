import pandas as pd
import numpy as np
import random


class satellite_object:
    ###larger image that contains info on all of the satellites
    def __init__(self, name, description, coords, classtype, direction, velocity):
        #name of satellite
        self.name = name
        #brief description
        self.description = description
        #tuple coordinates
        self.coords = coords
        ###which type of satellite is it? Base types include: transport, fixed, and junk (space junk)
        self.classtype = classtype
        ###direction of travel (normalised vector)
        self.direction = direction
        ###velocity - we can calculate this later from height above earths surface, but now have this as an input
        self.velocity = velocity
    def validate_coords(self):
        ###we need to ensure the coordinates are in xyz tuple form
        coords = self.coords
        try:
            assert type(coords)==tuple
            x_ = coords[0]
            y_ = coords[1]
            z_ = coords[2]
            for coord in [x_, y_, z_]:
                assert type(coord)==float
            r = np.sqrt(x_**2 +y_**2 + z_**2)
            ###assert that the radius is indeed in low earth orbit
            assert (r > 6571) & (r<8371), "incorrect coordinates, creating new ones"
        except AssertionError:
            ### if no / incorrect coordinates are given, a dummy coordinate system will be given
            ### note - coordinates are defined in x, y, z geocentric coordinates above the earth's center core
            ### Earths radius is 6371 kilometers. Low earth orbit is defined as 200-2000 kilometers
            ### above earths surface. We'll create randomized x, y, and z, such that x2+y2+z2 > 6571

            #step 1, create random vector r above earth that satisfies low earth orbit
            r = np.random.uniform(low = 6571, high = 8371, size = 1)
            #choose random x 
            x = np.random.uniform(low = -1*r, high = r, size = 1)
            #choose random y
            y = np.random.uniform(low = -1 * np.sqrt(r**2 - x**2), high = np.sqrt(r**2 - x**2), size = 1)
            # z will come naturally from pythagorean theorem
            z = np.random.choice([-1*(r**2 - x**2 - y**2), (r**2 - x**2 - y**2)])
            self.coords = (x, y, z)
    def validate_direction(self):
        direction = self.direction
        try:
            assert type(direction)==tuple
            x_ = direction[0]
            y_ = direction[1]
            z_ = direction[2]
            for coord in [x_, y_, z_]:
                assert type(coord)==float
            ###assert that the direction is a normalised vector
            assert (r==1), "incorrect directions, creating new ones"
        except AssertionError:
            ### if no / incorrect direction tuple is given, a dummy coordinate system will be given
            #step 1, create random vector r above earth that satisfies low earth orbit
            r = 1
            #choose random x 
            x = np.random.uniform(low = -1, high = 1, size = 1)
            #choose random y
            y = np.random.uniform(low = -np.sqrt(1 - x**2), high = np.sqrt(1 - x**2), size = 1)
            # z will come naturally from pythagorean theorem
            z = np.random.choice([-1*(r**2 - x**2 - y**2), (r**2 - x**2 - y**2)])
            self.direction = (x, y, z)


    def move_stationary(self, time):
        ###movement of satellite object due to acceleration moving around the earths core
        ###additional acceleration will be calculated later on
        ###recall earths circumference is 40000 km
        ###also note that to preserve radius above earth, we will have to change the direction
        ###of travel afterwards

        #time is in seconds
        #velocity is in km/s

        ###importing necessary variables
        coords = self.coords
        direction = self.direction
        velocity = self.velocity
        ###distance travelled in spherical polar coordinates
        distance_travelled = velocity * time

        x_travelled = (direction[0]) * (distance_travelled)
        y_travelled = (direction[1]) * (distance_travelled)
        z_travelled = (direction[2]) * (distance_travelled)

        new_coord_x = coords[0] + x_travelled
        new_coord_y = coords[1] + y_travelled
        new_coord_z = coords[2] + z_travelled

        new_coords = tuple([new_coord_x, new_coord_y, new_coord_z])

        old_coord_x = coords[0]
        old_coord_y = coords[1]
        old_coord_z = coords[2]
        
        r = np.abs(np.sqrt(old_coord_x**2 + old_coord_y**2 + old_coord_z**2))
        r_check = np.abs(np.sqrt(new_coord_x**2 + new_coord_y**2 + new_coord_z**2))

        ###Note! We cant have a satellite go 'infinitely' off in a different direction
        ###The new location will change the direction of travel to maintain a constant radius
        ###above the earths surface

        ###first calculating the relevant angles
        theta_old = np.arctan(old_coord_x/old_coord_y)
        theta_new = np.arctan(new_coord_x/new_coord_y)
        phi_old = np.arccos(old_coord_z/r)
        phi_new = np.arccos(new_coord_z/r)

        ###calculate new directions
        new_direction_x = direction[0] * (np.sin(phi_new)* np.cos(theta_new))/(np.sin(phi_old) * np.cos(theta_old))
        new_direction_y = direction[1] * (np.sin(phi_new)* np.sin(theta_new))/(np.sin(phi_old) * np.sin(theta_old))
        new_direction_z = direction[2] * (np.cos(phi_new)/np.cos(phi_old))

        new_direction = tuple([new_direction_x, new_direction_y, new_direction_z])
        ###this needs testing!

        self.direction = new_direction
        self.coords = new_coords
        self.velocity = velocity

        return







