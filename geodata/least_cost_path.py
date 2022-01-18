import sys, os
try:
    sys.path.append("C:\\GitHub\\hy-geo-utils\\")
    from geo_utils import raster2array, create_raster, get_srs, coords2offset
except:
    print("ERROR: No geo_utils.")

import gdal
from gdal import osr
from skimage.graph import route_through_array
import numpy as np

gdal.UseExceptions()


def create_path_array(raster_array, geo_transform, start_coord, stop_coord):
    # transform coordinates to array index
    try:
        start_index_x, start_index_y = coords2offset(geo_transform, start_coord[0], start_coord[1])
        stop_index_x, stop_index_y = coords2offset(geo_transform, stop_coord[0], stop_coord[1])
    except TypeError:
        print("ERROR: Could not calculate coordinate offset (see previous messages).")
        return None
    # replace np.nan with max raised by an order of magnitude to exclude pixels from least cost
    raster_array[np.isnan(raster_array)] = np.nanmax(raster_array) * 10

    # create path
    try:
        index_path, cost = route_through_array(raster_array, (start_index_y, start_index_x),
                                               (stop_index_y, stop_index_x),
                                               geometric=True, fully_connected=True)
    except TypeError:
        print("ERROR: route_through_array encountered a problem.")
        return None

    index_path = np.array(index_path).T
    path_array = np.zeros_like(raster_array)
    path_array[index_path[0], index_path[1]] = 1
    return path_array


def identify_path(in_file_name, out_file_name, start_coord, stop_coord):
    print("reading raster")
    try:
        src_raster, raster_array, geo_transform = raster2array(in_file_name)  # creates array from cost surface raster
    except TypeError:
        print("ERROR: raster to array conversion failed (check earlier error messages).")
        return None
    try:
        path_array = create_path_array(raster_array, geo_transform, start_coord, stop_coord)  # creates path array
    except TypeError:
        print("ERROR: Failed to create array of path check earlier error messages).")
        return None

    src_srs = get_srs(src_raster)
    create_raster(out_file_name, path_array, epsg=int(src_srs.GetAuthorityCode(None)),
                  rdtype=gdal.GDT_Byte, geo_info=geo_transform)


if __name__ == "__main__":
    in_file_name = r"" + os.path.abspath('') + "/river-architect/slope-percent.tif"
    start_coord = (6749261.94092826917767525, 2206970.35179582564160228)
    stop_coord = (6749016.82820663042366505, 2207050.61491037486121058)
    out_file_name = r"" + os.path.abspath('') + "/river-architect/least_cost.tif"
    identify_path(in_file_name, out_file_name, start_coord, stop_coord)
