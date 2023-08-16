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

        # Time period indexing is going to start at intervals 0, 120, 240, 360, 480
        # Each interval will cover 11 years, even though the time period length is 10
        # Indexing lengths will be 132 since each index represents one month, we have 11 * 12 = 132 for 11 years of data
        # Intervals for a 51 year file split into 5 time periods:
        # 0   - 132
        # 120 - 252
        # 240 - 372
        # 360 - 492
        # 480 - 612
        # The intervals will overlap by one year while averaging, but they are all equal in length (132 = 11 * 12 -> 11 years of data)
        
        try:
            
            file = "netcdf_files_full/test_data_4000-4050.nc"
            self.ds = xr.open_dataset(file, decode_times=False)

            start = (time_period * self.time_period_length * 12)
            end = start + ((self.time_period_length + 1) * 12)

            total_data = self.ds.TS[start : end]

            averaged_data = total_data[0]


            for i in range(1, len(total_data)):
                averaged_data += total_data[i]

            self.ds.close()

            averaged_data = averaged_data / len(total_data)

            return averaged_data

        # AttributeError: attribute T was not found in the file
        except AttributeError:
            print("Dataset is missing \'TS\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()


if __name__=='__main__':
    testPlot = TemperatureSurfacePlot(months=['01', '04', '07'], time_periods=['0', '4'])
    testPlot.set_data()
