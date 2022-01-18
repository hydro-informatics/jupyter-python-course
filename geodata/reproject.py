from shp_mgmt import *

shp_driver = ogr.GetDriverByName("ESRI Shapefile")

# open input shapefile and layer
in_shp = shp_driver.Open(r"" + os.path.abspath('') + "/shapefiles/countries.shp")
in_shp_lyr = in_shp.GetLayer()

# get input SpatialReference
in_sr = osr.SpatialReference(str(in_shp_lyr.GetSpatialRef()))
# auto-detect epsg
in_sr.AutoIdentifyEPSG()
# assign input SpatialReference
in_sr.ImportFromEPSG(int(in_sr.GetAuthorityCode(None)))

# create SpatialReference for new shapefile
out_sr = osr.SpatialReference()
out_sr.ImportFromEPSG(3857)

# create a CoordinateTransformation object
coord_trans = osr.CoordinateTransformation(in_sr, out_sr)

# create output shapefile and get layer
out_shp = create_shp(r"" + os.path.abspath('') + "/shapefiles/country_web.shp", layer_name="basemap", layer_type="line")
out_shp_lyr = out_shp.GetLayer()

# look up layer (features) definitions in input shapefile
in_lyr_def = in_shp_lyr.GetLayerDefn()
# copy field names of input layer attribute table to output layer
for i in range(0, in_lyr_def.GetFieldCount()):
    out_shp_lyr.CreateField(in_lyr_def.GetFieldDefn(i))

# instantiate feature definitions object for output layer (currently empty)
out_shp_lyr_def = out_shp_lyr.GetLayerDefn()

# iteratively append all input features in new projection
in_feature = in_shp_lyr.GetNextFeature()
while in_feature:
    # get the input geometry
    geometry = in_feature.GetGeometryRef()
    # re-project (transform) geometry to new system
    geometry.Transform(coord_trans)
    # create new output feature
    out_feature = ogr.Feature(out_shp_lyr_def)
    # assign in-geometry to output feature and copy field values
    out_feature.SetGeometry(geometry)
    for i in range(0, out_shp_lyr_def.GetFieldCount()):
        out_feature.SetField(out_shp_lyr_def.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))
    # add the feature to the shapefile
    out_shp_lyr.CreateFeature(out_feature)
    # prepare next iteration
    in_feature = in_shp_lyr.GetNextFeature()

# release shapefiles and layers
in_shp = None
in_shp_lyr = None
out_shp = None
out_shp_lyr = None

# create .prj file for  output shapefile for web application references
with open(r"" + os.path.abspath('') + "/shapefiles/country_web.prj", "w+") as prj:
    prj.write(get_wkt(3857))