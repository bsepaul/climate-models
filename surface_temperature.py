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

class SurfaceTemperaturePlot(Plot):

    def __init__(self, months, color="viridis", central_longitude=0):

        # Initiate instance of super class: Plot
        super().__init__(months, color, central_longitude, "Global Surface Temperature", "K", "sfc_temp_plot.pdf")


    def set_data(self):

        # get the data from the first month in the list of months
        first_month = self.months[0]
        file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(
            first_month)
        self.ds = xr.open_dataset(file, decode_times=False)
        print("collecting data from file: {}".format(file))
        
        try:
            # Go through each month's file and sum  precipitation values, TMQ
            for month in self.months[1:]:
                file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(
                    month)
                print("collecting data from file: {}".format(file))
                next_ds = xr.open_dataset(file, decode_times=False)
                self.ds.TS.values += next_ds.TS.values

            self.data = self.ds.TS
            self.ds.close()

        # AttributeError: attribute TS was not found in the file
        except AttributeError:
            print("Dataset is missing \'TS\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()

        # Average the values by dividing the values by the number of months
        self.data.values = (self.data.values) / len(self.months)