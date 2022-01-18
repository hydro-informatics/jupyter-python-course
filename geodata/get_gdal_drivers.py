import gdal


# instantiate driver count object (iterable numeric)
driver_list = []
for i in range(gdal.GetDriverCount()):
    driver_list.append(str(gdal.GetDriver(i).ShortName))

# sort driver list alphabetically
driver_list.sort()

# print driver list (comma separated list)
print(", ".join(driver_list))
