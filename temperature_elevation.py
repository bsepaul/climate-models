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
# current shape = (12, 30, 96, 144)

class ElevationTemperature(Plot):

    def __init__(self, months, elevation, color="viridis", central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, color, central_longitude, "Global Elevation Temperature Difference", "K", "temp_elev_plot.pdf")

        self.elevation = elevation
        self.ds_a = None
        self.ds_b = None

        # The files contain all 12 months' data so we are indexing the data differently
        # Subtracting 1 because month "04" is April, which is indexed by 3
        self.months = [(int(month)-1) for month in self.months]

    def set_data(self):

        try:

            # define two files needed to compare data
            file_a = 'netcdf_files_full/b.ie12.B1850.f19_g16.PMIP4-pliomip2.ecc_0.013216480.obliq_22.41968.CO2_283.9966.cam.h0.0500.nc'
            file_b = 'netcdf_files_full/b.ie12.B1850.f19_g16.PMIP4-pliomip2.ecc_0.018253007.obliq_23.23545.CO2_556.8582.cam.h0.0500.nc'

            # get data for both files
            self.ds_a = xr.open_dataset(file_a, decode_times=False)
            self.ds_b = xr.open_dataset(file_b, decode_times=False)

            # extract values for the elevation selected by the user
            data_a = self.ds_a.T[:, self.elevation]
            data_b = self.ds_b.T[:, self.elevation]

            # get first month
            first_month = self.months[0]

            # sum together values for all selected months
            for month in self.months[1:]:
                data_a.values[first_month] += data_a.values[month]
                data_b.values[first_month] += data_b.values[month]

            # get the average by dividing by the length of month list
            data_a.values[0] = data_a.values[first_month] / len(self.months)
            data_b.values[0] = data_b.values[first_month] / len(self.months)

            # store the difference of the data sets in self.data to be used for plotting
            self.data = data_a - data_b

            # close datasets
            self.ds_a.close()
            self.ds_b.close()

        # AttributeError: attribute T was not found in the file
        except AttributeError:
            print("Dataset is missing \'T\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()