import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt
import math
# import mpld3

class PrecipitationPlot:

    def __init__(self, type, months, color="viridis", central_longitude=0):
        self.type   = type   # type will specify whether this is precipitation rate or precipitation amount
        self.ds     = None   # ds is the data from the files
        self.data   = None   # data will store the data that the graph is going to be made from
        self.months = months # months is an array of the months that the user wants to be averaged for their plot
        self.label  = ""     # label of the units on color bar
        self.title  = ""     # title of the plot
        self.color  = color  # color scheme of the plot
        self.central_longitude = central_longitude

    def set_data(self):

        # get the data from the first month in the list of months
        first_month = self.months[0]
        file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(first_month)
        self.ds = xr.open_dataset(file, decode_times=False)
        print("collecting data from file: {}".format(file))

        # If we are making a graph of the rate of precipitation
        if self.type == "rate":
            self.label = "1e -7 m/s"
            self.title = "Precipitation Rates" 
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

        # If we are making a graph of the amount of precipitation
        elif self.type == "amount":
            self.label = "kg/m2"
            self.title = "Precipitation Amount" 
            try:
                # Go through each month's file and sum  precipitation values, TMQ
                for month in self.months[1:]:
                    file = "netcdf_files_full/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(month)
                    print("collecting data from file: {}".format(file))
                    next_ds = xr.open_dataset(file, decode_times=False)
                    self.ds.TMQ.values += next_ds.TMQ.values

                # Average the values by dividing the values by the number of months
                self.data = self.ds.TMQ

            # AttributeError: attribute PRECC or PRECL was not found in the file
            except AttributeError:
                print("Dataset is missing either \'PRECC\' or \'PRECL\' attribute")
                exit()
            
            # Another error occurred while accessing the data
            except:
                print("Something went wrong while accessing the data file: {}".format())
                exit()

        # Average the values by dividing the values by the number of months
        self.data.values = (self.data.values) / len(self.months)


    def make_fig(self):

        max = min = self.data.values[0][0][0]
        for chunk in self.data.values:
            for temps in chunk:
                for temp in temps:
                    if temp > max: max = temp
                    elif temp < min: min = temp
        max = math.ceil(max)
        min = math.floor(min)

        fig = plt.figure(figsize=(9,6))
        # ax = plt.axes(projection=ccrs.PlateCarree())
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=self.central_longitude))

        # add coastlines
        ax.coastlines(linewidths=0.5)
        # ax.add_feature(cfeature.LAND, facecolor="lightgray")

        ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())

        # Use geocat.viz.util convenience function to set axes limits & tick values
        gv.set_axes_limits_and_ticks(ax,
                                     xlim=(-180, 180),
                                     ylim=(-90, 90),
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-90, 90, 7))

        # plot the first time slice
        self.data[0, :, :].plot.contourf(ax=ax,
                                        transform=ccrs.PlateCarree(),
                                        vmin=0,
                                        vmax = max,
                                        # levels = 10,
                                        levels = max*20 if (self.type == "rate") else max*2, # number of different precipitation levels
                                        cmap = self.color,
                                        cbar_kwargs = {
                                            "extendrect":True,
                                            "orientation":"horizontal",
                                            "spacing":"proportional",
                                            "format":"%.2f" if (self.type == "rate") else "%.1f",
                                            # "ticks": np.arange(0, (max), (max/10)),
                                            # "ticks": np.arange(0, (max+1), (max/10)),
                                            "label": self.label,
                                            "shrink": 0.90})
                                            # "pad": 0.08})

        # Use geocat.viz.util convenience function to add minor and major tick lines
        gv.add_major_minor_ticks(ax, labelsize=10)

        # Use geocat.viz.util convenience function to make latitude, longitude tick labels
        gv.add_lat_lon_ticklabels(ax)

        gv.set_titles_and_labels(
            ax=ax,
            maintitle=self.title,
            maintitlefontsize="16",
            xlabel="Latitude",
            ylabel="Longitude")

        return fig
        # html_str = mpld3.fig_to_html(fig)
        # Html_file= open("index.html","w")
        # Html_file.write(html_str)
        # Html_file.close()

        # plt.show()

    def create_plot(self):
        self.set_data()
        self.make_fig()

# Only test if running this file
if __name__ == '__main__':
    testPlot = PrecipitationPlot(type="amount", months=["01", "02", "03", "04"])
    testPlot.set_data()
    fig = testPlot.make_fig()
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    graph = f"<img src='data:image/png;base64,{data}'/>"

    with open('test.html', 'w', encoding='utf-8') as file:
        file.writelines(graph)