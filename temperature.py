import numpy as np
import cartopy.crs as ccrs
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt


class TemperaturePlot:

    def __init__(self, months, color="viridis", central_longitude=0):
        self.ds = None   # ds is the data from the files
        self.data = None   # data will store the data that the graph is going to be made from
        # months is an array of the months that the user wants to be averaged for their plot
        self.months = months
        self.label = ""     # label of the units on color bar
        self.title = ""     # title of the plot
        self.color = color  # color scheme of the plot
        self.central_longitude = central_longitude

    def set_data(self):

        # get the data from the first month in the list of months
        first_month = self.months[0]
        file = "netcdf_files/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(
            first_month)
        self.ds = xr.open_dataset(file, decode_times=False)
        print("collecting data from file: {}".format(file))
        self.label = "K"
        self.title = "Global Surface Temperature"
        try:
            # Go through each month's file and sum  precipitation values, TMQ
            for month in self.months[1:]:
                file = "netcdf_files/b.e12.B1850.T31_g37.1x.cam.h0.3000-{}.nc".format(
                    month)
                print("collecting data from file: {}".format(file))
                next_ds = xr.open_dataset(file, decode_times=False)
                self.ds.TS.values += next_ds.TS.values

            self.data = self.ds.TS

        # AttributeError: attribute PRECC or PRECL was not found in the file
        except AttributeError:
            print("Dataset is missing \'TS\' attribute")
            exit()

        # Another error occurred while accessing the data
        except:
            print("Something went wrong while accessing the data file")
            exit()

        # Average the values by dividing the values by the number of months
        self.data.values = (self.data.values) / len(self.months)

    def make_graph(self):
        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree(
            central_longitude=self.central_longitude))

        # add coastlines
        ax.coastlines(linewidths=0.5)

        ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())

        # Use geocat.viz.util convenience function to set axes limits & tick values
        gv.set_axes_limits_and_ticks(ax,
                                     xlim=(-180, 180),
                                     ylim=(-90, 90),
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-90, 90, 7))

        # Use geocat.viz.util convenience function to add minor and major tick lines
        gv.add_major_minor_ticks(ax, labelsize=10)

        # Use geocat.viz.util convenience function to make latitude, longitude tick labels
        gv.add_lat_lon_ticklabels(ax)

        plot = self.data[0, :, :].plot.contourf(ax=ax,
                                                transform=ccrs.PlateCarree(),
                                                levels=120,
                                                cmap=self.color,
                                                add_colorbar=False)

        cbar = plt.colorbar(plot,
                            orientation='horizontal',
                            shrink=0.9,
                            extendrect=True)

        cbar.ax.tick_params(labelsize=10)

        gv.set_titles_and_labels(
            ax=ax,
            maintitle="Global Surface Temperature (K)",
            xlabel="Longitude",
            ylabel="Latitude")

        fig.savefig('static/plot2.png')

    def create_plot(self):
        self.set_data()
        self.make_graph()


testPlot = TemperaturePlot(["01", "02", "03", "04"])
testPlot.create_plot()
