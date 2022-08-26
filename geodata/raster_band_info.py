from flusstools.geotools.raster_mgmt import *
# make sure to use exceptions
gdal.UseExceptions()


def how2use():
    # provide usage instructions for the script
    print("""
    $ raster_band_info.py [ band number ] input-raster
    """)
    # exit program if wrong input arguments provided
    sys.exit(1)


def get_color_bands(raster_band):
    """
    :param raster_band: osgeo.gdal.Band object
    :output: list of color bands used in raster_band
    """

    # get ColorTable and return False if None
    color_table = raster_band.GetColorTable()
    if color_table is None:
        print("Band has no ColorTable.")
        return None
    else:
        print("Found %i color definitions." % int(color_table.GetCount()))

    # iterate through color_table and append objects found to colors_bands list
    color_bands = []
    for c in range(0, color_table.GetCount()):
        entry = color_table.GetColorEntry(c)
        if not entry:
            continue
        color_bands.append(str(color_table.GetColorEntryAsRGB(c, entry)))
    return color_bands


def main(band_number, input_file):
    src, band = open_raster(input_file)
    print("Band minimum: ", band.GetMinimum())
    print("Band maximum: ", band.GetMaximum())
    print("No-data value: ", band.GetNoDataValue())
    print("Band unit type: ", band.GetUnitType())

    try:
        print(", ".join(get_color_bands(band)))
    except TypeError:
        print("ColorTable: None")


if __name__ == '__main__':
    # make standalone
    if len(sys.argv) < 3:
        print("""
        ERROR: Provide two arguments:
        1) the band number (int) and 2) input raster directory (str)
        """)
        print("Received: (1)" + str(sys.argv[1]) + " (2) " + str(sys.argv[2]))
        how2use()

    main(int(sys.argv[1]), str(sys.argv[2]))
