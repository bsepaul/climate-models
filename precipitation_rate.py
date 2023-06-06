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

class PrecipitationRatePlot(Plot):

    def __init__(self, months, color="viridis", central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, color, central_longitude, "Precipitation Rates", "1e -7 m/s", "precip_rate_plot.pdf")


    def set_data(self):

        # get the data from the first month in the list of months
        first_month = self.months[0]
        file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(first_month)
        self.ds = xr.open_dataset(file, decode_times=False)
        print("collecting data from file: {}".format(file))

        try:
            # Go through each month's file and sum both precipitation values, PRECC and PRECL
            for month in self.months[1:]:
                file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(month)
                print("collecting data from file: {}".format(file))
                next_ds = xr.open_dataset(file, decode_times=False)
                self.ds.PRECC.values += next_ds.PRECC.values
                self.ds.PRECL.values += next_ds.PRECL.values

            # Add PRECC and PRECL values
            self.data = self.ds.PRECC
            self.data.values += self.ds.PRECL.values
            self.data.values *= 10000000
        
        # AttributeError: attribute PRECC or PRECL was not found in the file
        except AttributeError:
            print("Dataset is missing either \'PRECC\' or \'PRECL\' attribute")
            exit()
        
        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file: {}".format(file))
            exit()

        # Average the values by dividing the values by the number of months
        self.data.values = (self.data.values) / len(self.months)