shp_dir = r"" + os.path.abspath('') + "/geodata/shapefiles/rivers.shp"
# print(shp_dir)
river_pts = create_shp(shp_dir, layer_name="basemap", layer_type="point")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_epsg_code(3857))
    prj.write(get_epsg_code(6864))  # results in the same!

# get basemap layer
lyr = river_pts.GetLayer()

# add string field "rivername"
field_gname = ogr.FieldDefn("rivername", ogr.OFTString)
lyr.CreateField(field_gname)

# names and coordinates of central EU rivers in EPSG:3857 WG84 / Pseudo-Mercator
pt_names = {"Aare": (916136.03, 6038687.72),
            "Ain": (623554.12, 5829154.69),
            "Inn": (1494878.95, 6183793.83)}

# add the three rivers as points to the basemap layer
for n in pt_names.keys():
    # create Feature as child of the layer
    pt_feature = ogr.Feature(lyr.GetLayerDefn())
    # define value n (river) in the rivername field
    pt_feature.SetField("rivername", n)
    # use WKT format to add a point geometry to the Feature
    wkt = "POINT(%f %f)" % (float(pt_names[n][0]), float(pt_names[n][1]))
    point = ogr.CreateGeometryFromWkt(wkt)
    pt_feature.SetGeometry(point)
    # append the new feature to the basement layer
    lyr.CreateFeature(pt_feature)

# release files
lyr = None
river_pts = None