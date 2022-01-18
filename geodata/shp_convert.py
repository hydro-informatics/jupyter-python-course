from gdal import ogr
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(1179091.1646903288, 712782.8838459781)
ring.AddPoint(1161053.0218226474, 667456.2684348812)
ring.AddPoint(1214704.933941905, 641092.8288590391)

poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

geojson = poly.ExportToJson()
print(geojson)