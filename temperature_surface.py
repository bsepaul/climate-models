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

# INFORMATION ON TS ATTRIBUTE FOR NETCDF DATA
# filling on, default _FillValue of 9.969209968386869e+36 used, 'TS': <class 'netCDF4._netCDF4.Variable'>
# float32 TS(time, lat, lon)
#     units: K
#     long_name: Surface temperature (radiative)
#     cell_methods: time: mean
# unlimited dimensions: time
# current shape = (612, 96, 144)

class TemperatureSurfacePlot(Plot):

    def __init__(self, months, time_periods, color="viridis", min_longitude=-180, max_longitude=180, min_latitude=-90, max_latitude=90, central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, time_periods, color, min_longitude, max_longitude, min_latitude, max_latitude, central_longitude, "Global Surface Temperature", "K", "sfc_temp_plot.pdf")

    def get_time_period_data(self, time_period):
        
        try:
            
            file = "netcdf_files_full/test_data_4000-4050.nc"
            self.ds = xr.open_dataset(file, decode_times=False)

        # Another error occurred while accessing the data
        except Exception as error:
            print("Something went wrong while accessing the data file. See error below:")
            print(error)
            exit()

        # Time period indexing is going to start at intervals 0, 120, 240, 360, 480
        # Each interval will cover 11 years, even though the time period length is 10
        # Indexing lengths will be 132 since each index represents one month, we have 11 * 12 = 132 for 11 years of data
        # Intervals for a 51 year file split into 5 time periods:
        # 0   - 132, 120 - 252, 240 - 372, 360 - 492, 480 - 612
        # The intervals will overlap by one year while averaging, but they are all equal in length (132 = 11 * 12 -> 11 years of data)
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
        selected_data = self.ds.TS.isel(time=[index for index in indexes])
        # Interpolate longitude values so it goes from (0, 357) -> (0, 360)
        selected_data = gv.xr_add_cyclic_longitudes(selected_data, "lon")
        # Select the latitude and longitude values based on min/max lat/lon values that user enters
        selected_data = selected_data.sel(lat=self.latitude_range, method='nearest', tolerance=2)
        selected_data = selected_data.sel(lon=self.longitude_range, method='nearest', tolerance=2)
        # Average the data over time variable
        selected_data = selected_data.mean('time')

        # Close the data set
        self.ds.close()

        # Return selected, interpolated, averaged data to be plotted
        return selected_data