def feet_to_meter(*args, **kwargs):
    """ 
    :param *args: numeric values in feet
    :output: returns list or float of input values in meter
    """
    value_list = []
    conversion_factor = 0.3048
    for k in kwargs.items():
            if "conv" in k[0]:
                try:
                    conversion_factor = float(k[1])
                    print("Using conversion factor = " + str(k[1]))
                except:
                    print(str(k[1]) + " is not a number (using default value 0.3048).")  
    
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + " is not a number.")
    if value_list.__len__() > 1:
        return value_list
    else:
        return value_list[0]
