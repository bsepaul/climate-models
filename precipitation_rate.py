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

# INFORMATION ON PRECC ATTRIBUTE FOR NETCDF DATA
# filling on, default _FillValue of 9.969209968386869e+36 used, 'PRECC': <class 'netCDF4._netCDF4.Variable'>
# float32 PRECC(time, lat, lon)
#     units: m/s
#     long_name: Convective precipitation rate (liq + ice)
#     cell_methods: time: mean
# unlimited dimensions: time
# current shape = (612, 96, 144)

# INFORMATION ON PRECL ATTRIBUTE FOR NETCDF DATA
# filling on, default _FillValue of 9.969209968386869e+36 used, 'PRECL': <class 'netCDF4._netCDF4.Variable'>
# float32 PRECL(time, lat, lon)
#     units: m/s
#     long_name: Large-scale (stable) precipitation rate (liq + ice)
#     cell_methods: time: mean
# unlimited dimensions: time
# current shape = (612, 96, 144)

class PrecipitationRatePlot(Plot):

    def __init__(self, months, time_periods, color="viridis", min_longitude=-180, max_longitude=180, min_latitude=-90, max_latitude=90, central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, time_periods, color, min_longitude, max_longitude, min_latitude, max_latitude, central_longitude, "Precipitation Rate", "mm/day", "precip_rate_plot.pdf")

    def get_time_period_data(self, time_period):

        try:

            file = "netcdf_files_full/test_data_4000-4050.nc"
            self.ds = xr.open_dataset(file, decode_times=False)

            start = (time_period * self.time_period_length * 12)
            end = start + ((self.time_period_length + 1) * 12)

            total_data = self.ds.PRECC[start : end] + self.ds.PRECL[start : end]

            mean_data = total_data.mean('time')

            mean_interpolated_data = gv.xr_add_cyclic_longitudes(mean_data, "lon")
            mean_interpolated_data *= 86400000

            self.ds.close()

            return mean_interpolated_data

        # AttributeError: attribute T was not found in the file
        except AttributeError:
            print("Dataset is missing \'PRECC\' or \'PRECL\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()