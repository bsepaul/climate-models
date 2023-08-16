import numpy as np
import cartopy.crs as ccrs
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
from netCDF4 import Dataset
from plot import Plot

# INFORMATION ON T ATTRIBUTE FOR NETCDF DATA
# filling on, default _FillValue of 9.969209968386869e+36 used, 'T': <class 'netCDF4._netCDF4.Variable'>
# float32 T(time, lev, lat, lon)
#     mdims: 1
#     units: K
#     long_name: Temperature
#     cell_methods: time: mean
# unlimited dimensions: time
# current shape = (612, 30, 96, 144)

class TemperatureElevation(Plot):

    def __init__(self, months, time_periods, elevation, color="viridis", min_longitude=-180, max_longitude=180, min_latitude=-90, max_latitude=90, central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, time_periods, color, min_longitude, max_longitude, min_latitude, max_latitude, central_longitude, "Global Elevation Temperature", "K", "temp_elev_plot.pdf")

        self.elevation = elevation

    def get_time_period_data(self, time_period):

        try:

            file = "netcdf_files_full/test_data_4000-4050.nc"
            self.ds = xr.open_dataset(file, decode_times=False)

            start = (time_period * self.time_period_length * 12)
            end = start + ((self.time_period_length + 1) * 12)

            total_data = self.ds.T[start : end, self.elevation]

            mean_data = total_data.mean('time')

            mean_interpolated_data = gv.xr_add_cyclic_longitudes(mean_data, "lon")

            self.ds.close()

            return mean_interpolated_data

        # AttributeError: attribute T was not found in the file
        except AttributeError:
            print("Dataset is missing \'T\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()