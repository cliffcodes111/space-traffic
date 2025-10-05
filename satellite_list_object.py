import pandas as pd
import numpy as np
import string
import random
###importing the object for individual satellites
from satellite_objects import satellite_object

class satellite_database:
    ###This class of objects will build out the database
    def __init__(self, input_mode, number, input_data):
        ###input mode is how we want to define the input data - is it downloaded from a nasa app csv file
        #  or is it randomly generated (for test purposes)
        self.input_mode = input_mode
        ###if random generated input, how many satellites do we want?
        if input_mode == "random_generated":
            self.number = number
        elif input_mode == "input_data":
            # if we are already inputting data in about satellites
            self.number = len(input_data)
        else:
            self.number = number
        self.input_data = input_data
    
    def build_input_data(self):
        ###if we are randomly generating input data, this function will do it
        input_mode = self.input_mode
        if input_mode == "random_generated":
            sat_df = pd.DataFrame()
            n_satellites = self.number
            for number in range(0, n_satellites):
                name = id_generator()
                description = "dummy_description"
                classtype = str(np.random.choice(['transport', 'fixed', 'junk'], 1)[0])
                ###building out coordinates (this will be beefy)
                coords = self.random_coordinates()
                direction = self.random_direction()
                ###velocity is in km^second
                velocity = np.random.uniform(low = 6.9, high = 7.7, size = 1)[0]
                ###altitude is the radius of orbit - earths radius
                altitude = np.sqrt(coords[0]**2 + coords[1]**2 + coords[2]**2) - 6371
                ###now, building out a dataframe
                new_dict = {'name':name, 'description': description, 'classtype':classtype,\
                            'coordinate_x':coords[0], 'coordinate_y': coords[1], 'coordinate_z': coords[2], \
                            'direction_x':direction[0], 'direction_y':direction[1], 'direction_z': direction[2], \
                            'velocity':velocity, 'altitude': altitude}
                new_df = pd.DataFrame(data = new_dict, index = [name])
                sat_df = pd.concat([sat_df, new_df])
            ###set t=0
            sat_df['time'] = 0
            self.sat_data = sat_df
        elif input_mode == "input_data":
            print("data already present")
        else:
            print("incorrect random generated mode")
        return
    
    def move_by_one_second(self):
        ###move all the satellites their respective distances by one second
        time = 1 # 1 second
        sat_df = self.sat_data
        new_sat_data = pd.DataFrame()

        for index, row in sat_df.iterrows():
            the_time = row['time']+ time
            name = row['name']
            description = row['description']
            classtype = row['classtype']
            coords = tuple([row['coordinate_x'], row['coordinate_y'], row['coordinate_z']])
            direction = tuple([row['direction_x'], row['direction_y'], row['direction_z']])
            velocity = row['velocity']

            point_object = satellite_object(name, description, coords, classtype, direction, velocity)
            point_object.move(time = 1)
            new_coords = point_object.coords
            new_direction = point_object.direction

            new_sat_dict = {'name':name, 'description': description, 'classtype':classtype,\
                            'coordinate_x':new_coords[0], 'coordinate_y': new_coords[1], 'coordinate_z': new_coords[2], \
                            'direction_x':new_direction[0], 'direction_y':new_direction[1], 'direction_z': new_direction[2], \
                            'velocity':velocity, 'altitude': row['altitude'], 'time':the_time}
            new_sat_df = pd.DataFrame(data = new_sat_dict, index = [name])
            new_sat_data = pd.concat([new_sat_data, new_sat_df])

        self.sat_data = new_sat_data

        return
    def return_full_dataframe(self):
        ###simple function to return the entire dataset
        return_df = self.sat_data
        return return_df

    def random_coordinates(self):
        ###this function will build out randomly generated coordinates for proper low earth orbit
        #step 1, create random vector r above earth that satisfies low earth orbit
        r = np.random.uniform(low = 6571, high = 8371, size = 1)
        #choose random x 
        x = np.random.uniform(low = -1*r, high = r, size = 1)
        #choose random y
        y = np.random.uniform(low = -1 * np.sqrt(r**2 - x**2), high = np.sqrt(r**2 - x**2), size = 1)
        # z will come naturally from pythagorean theorem
        z = np.random.choice([-1*np.sqrt((r**2 - x**2 - y**2))[0], np.sqrt(r**2 - x**2 - y**2)[0]], size = 1)
        coords = tuple([x[0], y[0], z[0]])
        return coords
    
    def random_direction(self):
        ###this function will build out randomly generated vector directions
        #step 1, create random vector r that is normalised
        r = 1
        #choose random x 
        x = np.random.uniform(low = -1, high = 1, size = 1)
        #choose random y
        y = np.random.uniform(low = -np.sqrt(1 - x**2), high = np.sqrt(1 - x**2), size = 1)
        # z will come naturally from pythagorean theorem
        z = np.random.choice([-1*np.sqrt((r**2 - x**2 - y**2))[0], np.sqrt(r**2 - x**2 - y**2)[0]], size = 1)
        direction = tuple([x[0], y[0], z[0]])
        return direction

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    #to randomly generate satellite names
    return ''.join(random.choice(chars) for _ in range(size))

def test_satellite_database(total_time = 10):
    object = satellite_database("random_generated", 5, pd.DataFrame())
    object.build_input_data()
    total_df = pd.DataFrame()
    for time in range(1, total_time):
        object.move_by_one_second()
        df = object.return_full_dataframe()
        total_df = pd.concat([total_df, df])
    total_df.to_csv("sc_check_data")

    return

if __name__ == '__main__':
    test_satellite_database()