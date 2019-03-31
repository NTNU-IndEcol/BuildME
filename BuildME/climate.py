"""
Scripts for managing climate data

Copyright: Niko Heeren, 2019
"""
import pandas as pd


def read_epw(epw_file):
    """
    Returns a DataFrame with the climate data from the epw climate file.
    :param epw_file: path and filename of the epw file
    :return: pandas dataframe
    """
    epw_header = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Data Source and Uncertainty Flags', 'Dry Bulb Temperature',
                  'Dew Point Temperature', 'Relative Humidity', 'Atmospheric Station Pressure',
                  'Extraterrestrial Horizontal Radiation', 'Extraterrestrial Direct Normal Radiation',
                  'Horizontal Infrared Radiation Intensity', 'Global Horizontal Radiation', 'Direct Normal Radiation',
                  'Diffuse Horizontal Radiation', 'Global Horizontal Illuminance', 'Direct Normal Illuminance',
                  'Diffuse Horizontal Illuminance', 'Zenith Luminance', 'Wind Direction', 'Wind Speed',
                  'Total Sky Cover', 'Opaque Sky Cover', 'Visibility', 'Ceiling Height', 'Present Weather Observation',
                  'Present Weather Codes', 'Precipitable Water', 'Aerosol Optical Depth', 'Snow Depth',
                  'Days Since Last Snowfall', 'Albedo', 'Liquid Precipitation Depth', 'Liquid Precipitation Quantity']

    # https://stackoverflow.com/a/34028755/2075003
    with open(epw_file) as f:
        pos = 0
        cur_line = f.readline()
        while not cur_line.startswith("DATA"):
            pos = f.tell()
            cur_line = f.readline()
        f.seek(pos)
        f.readline()
        epw = pd.read_csv(f, header=None, names=epw_header)
    return epw
