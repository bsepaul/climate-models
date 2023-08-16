import numpy as np
import cartopy.crs as ccrs
import geocat.viz as gv
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import base64
from io import BytesIO
from netCDF4 import Dataset
import math

class Plot:

    def __init__(self, months, time_periods, color="viridis", min_longitude=-180, max_longitude=180, min_latitude=-90, max_latitude=90, central_longitude=0, title="Plot", label="", file_name="plot.pdf"):

        # Set the passed in variables
        self.months             = months            # months is an array of the months that the user wants to be averaged for their plot
        self.time_periods       = time_periods      # time_periods is an array of the time_period(s) that the user selected - one time_period means average of that time period, two time_periods means the difference of the average of each time period
        self.time_period_length = 10                # this could be passed in as a dynamic variable but set to 10 for now
        self.color              = color             # color scheme of the plot
        self.central_longitude  = central_longitude # longitude that will be at the center of rendered plot
        self.title              = title             # title of the plot
        self.label              = label             # label (units) of the plot
        self.file_name          = file_name         # file name of rendered plot if user saves the plot

        self.ds   = None    # ds will store the data from the files
        self.data = None    # data will store the data that the graph is going to be made from

        self.min_longitude = min_longitude  # user's entered value for minimum longitude value, defaults to -180
        self.max_longitude = max_longitude  # user's entered value for maximum longitude value, defaults to 180
        self.min_latitude  = min_latitude   # user's entered value for minimum latitude value, defaults to -90
        self.max_latitude  = max_latitude   # user's entered value for maximum latitude value, defaults to 90

        self.fig  = None    # fig will store the rendered graphical figure
        self.pdf  = None    # pdf will store the rendered pdf of the figure
        self.png  = None    # png will store the rendered png of the figure
        
        # Determine the width and height of the plot based on lat and lon values
        width = self.max_longitude - self.min_longitude
        height = self.max_latitude  - self.min_latitude

        # Determine the plot ratio by dividing by the min dimension
        # Ex: 20 x 100 is the same as a 10 x 50 -> both have plot ratios of 1 x 5
        self.width_ratio  = math.floor(width / min(width, height))
        self.height_ratio = math.floor(height / min(width, height))
        
        # Max number of ticks for both x and y axis is 12 ticks
        # If a plot has a 1 x 5 ratio 1 -> width_ratio and 5 -> height_ratio, we want less ticks on the x axis and more on the y axis
        # Either self.height_ratio or self.width_ratio = 1, dividing 12 by 1 gives us 12 and we want that for the larger dimension
        # We would get self.xticks = 12 / 5 = 2.4 and self.yticks = 12 / 1 = 12, after the ceiling function we have 3 ticks on the x axis and 12 on the y axis
        self.xticks = math.ceil(12 / self.height_ratio)
        self.yticks = math.ceil(12 / self.width_ratio)

        # We never want one tick because the user won't be able to tell the units, so increase it to 2
        if self.xticks == 1: self.xticks += 1
        if self.yticks == 1: self.yticks += 1

        # Get the first time period - there will always be a time_period_a since th euser must select at least one time period
        self.time_period_a = int(self.time_periods[0])
        # If the user has selected a second time period, the list of time periods will have a length of 2
        if len(self.time_periods) == 2:
            # Get the second time period
            self.time_period_b = int(self.time_periods[1])
            # If there are two time periods, it's a different plot so change the file name and plot title accordingly
            self.file_name = "diff_" + self.file_name
            self.title = self.title + " Difference"

    def set_data(self):

        if len(self.time_periods) <= 0:
            print("User needs to enter at least one time period to collect data for")
            exit()
        else:
            self.data = self.get_time_period_data(self.time_period_a)
            if len(self.time_periods) == 2:
                self.data -= self.get_time_period_data(self.time_period_b)

    def make_fig(self):

        max = min = self.data.values[0][0]
        for values in self.data.values:
            for value in values:
                if value > max: max = value
                elif value < min: min = value
        max = math.ceil(max)
        min = math.floor(min)

        projection = ccrs.PlateCarree(central_longitude=self.central_longitude)
        self.fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(projection=projection))

        # add coastlines
        ax.coastlines(resolution='110m',color='black')

        ax.set_extent([self.min_longitude, self.max_longitude, self.min_latitude, self.max_latitude], ccrs.PlateCarree())

        # Use geocat.viz.util convenience function to set axes limits & tick values
        gv.set_axes_limits_and_ticks(ax,
                                     xlim=(self.min_longitude, self.max_longitude),
                                     ylim=(self.min_latitude, self.max_latitude),
                                     xticks=np.linspace(self.min_longitude, self.max_longitude, self.xticks).round(2),
                                     yticks=np.linspace(self.min_latitude, self.max_latitude, self.yticks).round(2))

        plot = self.data[:, :].plot.contourf(ax=ax,
                                        transform=ccrs.PlateCarree(),
                                        vmin=min,
                                        vmax = max,
                                        levels = 20,
                                        cmap = self.color,
                                        cbar_kwargs = {
                                            "extendrect":True,
                                            "orientation":"horizontal",
                                            "spacing":"proportional",
                                            "format":"%.2f",
                                            "label": self.label,
                                            "shrink": 0.90})

        # Use geocat.viz.util convenience function to add minor and major tick lines
        gv.add_major_minor_ticks(ax, labelsize=8)

        # Use geocat.viz.util convenience function to make latitude, longitude tick labels
        gv.add_lat_lon_ticklabels(ax)

        gv.set_titles_and_labels(
            ax=ax,
            maintitle=self.title,
            maintitlefontsize="14",
            xlabel="Longitude",
            ylabel="Latitude",
            labelfontsize="10")

    def make_pdf(self):

        # Save figure in pdf form to a temporary buffer
        buf_pdf = BytesIO()
        self.fig.savefig(buf_pdf, format="pdf")

        # Embed the result in the html output
        data = base64.b64encode(buf_pdf.getbuffer()).decode("ascii")
        self.pdf = f"<a href='data:image/pdf;base64,{data}' title='Precipitation Plot pdf' download='{self.file_name}'>Download PDF of this graph</a>"
    
    def make_png(self):
        
        # Save figure in png form to a temporary buffer
        buf_png = BytesIO()
        self.fig.savefig(buf_png, format="png", dpi=1200)

        # Embed the result in the html output
        data = base64.b64encode(buf_png.getbuffer()).decode("ascii")
        self.png = f"<img class='graph-png' width='80%' src='data:image/png;base64,{data}'/>"

    def create_plot(self):
        self.set_data()
        self.make_fig()
        self.make_pdf()
        self.make_png()
