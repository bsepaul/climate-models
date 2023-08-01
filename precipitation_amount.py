import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt
import math
import base64
from io import BytesIO
from plot import Plot

# INFORMATION ON TMQ ATTRIBUTE FOR NETCDF DATA
# filling on, default _FillValue of 9.969209968386869e+36 used, 'TMQ': <class 'netCDF4._netCDF4.Variable'>
# float32 TMQ(time, lat, lon)
#     units: kg/m2
#     long_name: Total (vertically integrated) precipitable water
#     cell_methods: time: mean
# unlimited dimensions: time
# current shape = (612, 96, 144)

class PrecipitationAmountPlot(Plot):

    def __init__(self, months, time_periods, color="viridis", central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, time_periods, color, central_longitude, "Precipitation Amount", "kg/m2", "precip_amnt_plot.pdf")

    def get_time_period_data(self, time_period):

        try:

            file = "netcdf_files_full/test_data_4000-4050.nc"
            self.ds = xr.open_dataset(file, decode_times=False)

            start = (time_period * self.time_period_length * 12)
            end = start + ((self.time_period_length + 1) * 12)

            total_data = self.ds.TMQ[start : end]
            print(total_data)
            averaged_data = total_data[0]


            for i in range(1, len(total_data)):
                averaged_data += total_data[i]

            self.ds.close()

            averaged_data = averaged_data / len(total_data)

            return averaged_data

        # AttributeError: attribute T was not found in the file
        except AttributeError:
            print("Dataset is missing \'PRECC\' or \'PRECL\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()