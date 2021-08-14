import logging
import numpy as np
import pylas
import pickle

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)


def extract_point_coordinates(file_path: str, custom_file_name: str=None) -> str:
    """
    Function to open LAZ files that contain point cloud 
    coordinates as a 3D  numpy array into a pickled file 

    Args
    ----
    file_path : str
        path to laz or las file that contains lidar information

    custom_file_name : str, optional
        if set to none file will be relative to script file and be called "3d_points.pkl"
        custom file path for outputting point cloud coordinates, file must be a .pkl extention 

    Returns
    -------
    new_file_name : str
        name of new file where x, y, z point cloud coordinates were saved to
    """
    # open laz file to extract points
    las = pylas.read(file_path)
    # to get dimension names
    point_format = las.point_format
    # get length point list
    print(len(las.points))
    print(point_format.dimension_names)

    if not custom_file_name:
        # name for new file for numpy array points
        new_file_name = '3d_points.pkl'
    else:
        new_file_name = custom_file_name
    # extract points from oened file
    points = las.points
    # empty list to create numpy array with 
    point_list = []
    #iterate through list, convert from np.void to list, append to empty list
    for index, item in enumerate(points):
        point = list(item)[:3]
        point_list.append(point)
        print(f'Processing {len(points)} points: {round(((index/len(points)) * 100), 3)}% complete.')

    # create 3D numpy array of points
    np_point_list = np.array(point_list)
    # dump subset of data into new file, pickled for numpy array object
    with open( new_file_name, 'wb') as file:
        pickle.dump(np_point_list, file)
    logging.info(f'Points saved to: {new_file_name}')
    return new_file_name
