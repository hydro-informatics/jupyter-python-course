from shp_mgmt import *
from gdal import ogr
import pandas as pd
dreisam_inundation = pd.read_json(r"" + os.path.dirname(__file__) + "/json/hq100-dreisam.json")

shp_dir = r"" + os.path.dirname(__file__) + "/shapefiles/zzzpoly8.shp"

# print(shp_dir)
dreisam_hq100 = create_shp(shp_dir, layer_name="basemap", layer_type="polygon")

# create .prj file for the shapefile for GIS map applications
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_esriwkt(25832))

# get basemap layer
lyr = dreisam_hq100.GetLayer()

# add string field "tbg_name"
lyr.CreateField(ogr.FieldDefn("tbg_name", ogr.OFTString))

# add string field "area"
lyr.CreateField(ogr.FieldDefn("area", ogr.OFTReal))

for wkt, tbg in zip(dreisam_inundation["wkt_geom"], dreisam_inundation["TBG_NAME"]):
    # create Feature as child of the layer
    feature = ogr.Feature(lyr.GetLayerDefn())
    # assign tbg_name
    feature.SetField("tbg_name", tbg)
    # use WKT format to add a polygon geometry to the Feature
    polygon = ogr.CreateGeometryFromWkt(wkt)
    # define default value of 0 to the area field
    feature.SetField("area", polygon.GetArea())

    feature.SetGeometry(polygon)
    # append the new feature to the basement layer
    lyr.CreateFeature(feature)

lyr = None
a_new_shp_file = None
