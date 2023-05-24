from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure
from temperature import TemperaturePlot
from precipitation import PrecipitationPlot
import time
import mpld3
import numpy as np
import matplotlib.pyplot as plt


# function to create a dictionary of graph information so that it can be easily parsed through to render the correct graphs
def parse(html_data):

    # create an empty dictionary to store values selected by the user in the html form
    data = {"plots": [], "months": []}

    # lists of total possible selections
    plots = ["sfcTemp", "pcpRate", "pcpAmnt"]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    # find intersection of total list and user's selected list to parse out values and separate them for the dictionary
    data["plots"] = [plot for plot in html_data if plot in plots]
    data["months"] = [month for month in html_data if month in months]

    return data

# render the graphs into html strings
def render(html_data):

    data = parse(html_data)
    print(data)

    graphs = []

    for plot in  data["plots"]:
        print("User is requesting a {} plot for the months: {}".format(
            plot,  data["months"]))

        if plot == "sfcTemp":
            # Create surface temperature plot
            testPlot = TemperaturePlot( data["months"])

        elif plot == "pcpRate":
            # Create precipitation rate plot
            testPlot = PrecipitationPlot(type="rate", months= data["months"])
        
        elif plot == "pcpAmnt":
            # Create precipitation amount plot
            testPlot = PrecipitationPlot(type="amount", months= data["months"])

        # Set the data
        testPlot.set_data()

        # Get the figure
        fig = testPlot.make_fig()

        # ********** COMMENTED OUT TO TEST MPLD3 **********
        # # Save it to a temporary buffer.
        # buf = BytesIO()
        # fig.savefig(buf, format="png")

        # # Embed the result in the html output.
        # data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # graph = f"<img src='data:image/png;base64,{data}'/>"
        # *************************************************

        graph = mpld3.fig_to_html(fig)

        # Add the new graph to the list of graphs to be updated in the html file
        graphs.append(graph)


    # EXAMPLE PLOT
    xpoints = np.array([1, 8])
    ypoints = np.array([3, 10])

    plt.plot(xpoints, ypoints)
    fig = plt.figure(figsize=(9,6))
    plt.show()
    fig.savefig("sample_plt.png", format="png")
    graph = mpld3.fig_to_html(fig)
    graphs.append(graph)
    print(len(graphs))
    print(graphs[-1])

    return graphs