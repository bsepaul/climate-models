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
        
        # Another error occurred while accessing the data
        except Exception as error:
            print("Something went wrong while accessing the data file. See error below:")
            print(error)
            exit()

        start = (time_period * self.time_period_length * 12)
        end = start + ((self.time_period_length + 1) * 12)

        # Create a list of indexes to extract the data that the user is requesting
        # If the user requests the first time period, and months January, July, and December:
        # indexes = [0, 6, 11, 12, 18, 23, 24, 30, 35, 36, 42, 47, 48, 54, 59, 60, 66, 71, 72, 78, 83, 84, 90, 95, 96, 102, 107, 108, 114, 119, 120, 126, 131]
        indexes = []
        for jan_index in range(start, end, 12):
            for month_index in self.months:
                indexes.append(jan_index + month_index)

        # Select all of the time slices out of surface temperature data
        selected_data = self.ds.PRECC.isel(time=[index for index in indexes]) + self.ds.PRECL.isel(time=[index for index in indexes])
        # Interpolate longitude values so it goes from (0, 357) -> (0, 360)
        selected_data = gv.xr_add_cyclic_longitudes(selected_data, "lon")
        # Select the latitude and longitude values based on min/max lat/lon values that user enters
        selected_data = selected_data.sel(lat=self.latitude_range, method='nearest', tolerance=2)
        selected_data = selected_data.sel(lon=self.longitude_range, method='nearest', tolerance=2)
        # Average the data over time variable
        selected_data = selected_data.mean('time')
        # Convert from m/s to mm/day
        selected_data *= 86400000
        # Close the data set
        self.ds.close()

        # Return selected, interpolated, averaged data to be plotted
        return selected_data