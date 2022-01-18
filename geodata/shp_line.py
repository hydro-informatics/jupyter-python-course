from shp_mgmt import *

shp_dir = r"" + os.path.abspath('') + "/shapefiles/rhine_proxM.shp"

rhine_line = create_shp(shp_dir, layer_name="basemap", layer_type="line")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_wkt(3857))

# get basemap layer
lyr = rhine_line.GetLayer()

# coordinates for EPSG:3857 WG84 / Pseudo-Mercator
station_names = {"Basel": (844361.68, 6035047.42),
                 "Kembs": (835724.27, 6056449.76),
                 "Breisach": (842565.32, 6111140.43),
                 "Rhinau": (857547.04, 6158569.58),
                 "Strasbourg": (868439.31, 6203189.68)}

# create line object and add points from station names
line = ogr.Geometry(ogr.wkbLineString)
for stn in station_names.values():
    line.AddPoint(stn[0], stn[1])

# create field named "rives"
field_name = ogr.FieldDefn("river", ogr.OFTString)
lyr.CreateField(field_name)

# create feature, geometry, and field entry
line_feature = ogr.Feature(lyr.GetLayerDefn())
line_feature.SetGeometry(line)
line_feature.SetField("river", "Rhine")

# add feature to layer
lyr.CreateFeature(line_feature)

lyr = None
rhine_line = None