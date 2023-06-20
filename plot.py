import numpy as np
import cartopy.crs as ccrs
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
from netCDF4 import Dataset
import math

class Plot:

    def __init__(self, months, color="viridis", central_longitude=0, title="Plot", label="", file_name="plot.pdf"):

        # Set the passed in variables
        self.months            = months            # months is an array of the months that the user wants to be averaged for their plot
        self.color             = color             # color scheme of the plot
        self.central_longitude = central_longitude # longitude that will be at the center of rendered plot
        self.title             = title             # title of the plot
        self.label             = label             # label (units) of the plot
        self.file_name         = file_name         # file name of rendered plot if user saves the plot

        self.ds   = None    # ds will store the data from the files
        self.data = None    # data will store the data that the graph is going to be made from

        self.fig  = None    # fig will store the rendered graphical figure
        self.pdf  = None    # pdf will store the rendered pdf of the figure

    def set_data(self):
        pass

    def make_fig(self):

        max = min = self.data.values[0][0][0]
        for values in self.data.values[0]:
            for value in values:
                if value > max: max = value
                elif value < min: min = value
        max = math.ceil(max)
        min = math.floor(min)

        self.fig = plt.figure(figsize=(9,6))
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=self.central_longitude))

        # add coastlines
        ax.coastlines(linewidths=0.5)

        ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())

        # Use geocat.viz.util convenience function to set axes limits & tick values
        gv.set_axes_limits_and_ticks(ax,
                                     xlim=(-180, 180),
                                     ylim=(-90, 90),
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-90, 90, 7))

        # plot the first time slice
        plot = self.data[0, :, :].plot.contourf(ax=ax,
                                        transform=ccrs.PlateCarree(),
                                        vmin=min,
                                        vmax = max,
                                        levels = 30,
                                        cmap = self.color,
                                        cbar_kwargs = {
                                            "extendrect":True,
                                            "orientation":"horizontal",
                                            "spacing":"proportional",
                                            "format":"%.2f",
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
            xlabel="Longitude",
            ylabel="Latitude")

    def make_pdf(self):
        # Save it to a temporary buffer.
        buf = BytesIO()
        self.fig.savefig(buf, format="pdf")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        self.pdf = f"<a href='data:image/pdf;base64,{data}' title='Precipitation Plot pdf' download='{self.file_name}'>Download PDF of this graph</a>"

    def create_plot(self):
        self.set_data()
        self.make_fig()
        self.make_pdf()
