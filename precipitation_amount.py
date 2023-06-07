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
# current shape = (12, 96, 144)

class PrecipitationAmountPlot(Plot):

    def __init__(self, months, color="viridis", central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, color, central_longitude, "Precipitation Amount", "kg/m2", "precip_amnt_plot.pdf")


    def set_data(self):

        # get the data from the first month in the list of months
        first_month = self.months[0]
        file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(first_month)
        self.ds = xr.open_dataset(file, decode_times=False)
        print("collecting data from file: {}".format(file))

        try:
            # Go through each month's file and sum  precipitation values, TMQ
            for month in self.months[1:]:
                file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(month)
                print("collecting data from file: {}".format(file))
                next_ds = xr.open_dataset(file, decode_times=False)
                self.ds.TMQ.values += next_ds.TMQ.values

            # Average the values by dividing the values by the number of months
            self.data = self.ds.TMQ

        # AttributeError: attribute TMQ was not found in the file
        except AttributeError:
            print("Dataset is missing \'TMQ\' attribute")
            exit()
        
        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file: {}".format())
            exit()

        # Average the values by dividing the values by the number of months
        self.data.values = (self.data.values) / len(self.months)