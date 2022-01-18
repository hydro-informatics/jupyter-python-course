from gdal import ogr


# instantiate driver count object (iterable numeric)
driver_count = ogr.GetDriverCount()
driver_list = [] 

for i in range(driver_count):
    driver = ogr.GetDriver(i)
    driver_name = driver.GetName()
    if not driver_name in driver_list:
        driver_list.append(driver_name)

# sort driver list alphabetically
driver_list.sort()

# print driver list (comma separated list)
print(", ".join(driver_list))