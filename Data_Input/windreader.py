def windreader(file_in=None, speed_col=None, direction_col=None, file_out=None):
    """
    windDataReader reads a csv file containing wind data and returns a WindData object. It also saves the WindData
    object to file_out.
    Inputs:
        file_path_in     Path to a data file
        wind_speed       column number for wind speed data (should be provided in m/s)
        wind_direction   column number for wind direction data (should be provided in degrees East of North)
        time_col         column number of time data (should be provided in units of days)
        return           wind data object
    """
    import csv
    import pickle
    from inputclass import WindInfo
    
    file = open(file_in)
    data = csv.reader(file, delimiter=',')
    
    rows = [x for x in data]
    windlist = [x[speed_col] for x in rows]
    dirlist = [x[direction_col] for x in rows]
    
    wind = [float(i) for i in windlist]
    direction = [float(i) for i in dirlist]
        
    final = WindInfo(wind, direction)
    
    pickle.dump(final, open(file_out,'wb'))