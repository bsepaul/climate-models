from surface_temperature import SurfaceTemperaturePlot
from precipitation_amount import PrecipitationAmountPlot
from precipitation_rate import PrecipitationRatePlot
from temperature_elevation import ElevationTemperature
import mpld3

# render the graphs into html strings
def render(html_data):

    # create an empty dictionary to store values selected by the user in the html form
    data = {"plots": [], "months": [], "elevation": 0}

    # Attempt to extract user's selections from the html data
    # If user didn't select any months, return None
    data["months"] = html_data.getlist('month')
    if data["months"] == []: return None
    # If user didn't select any plot types, return None
    data["plots"]  = html_data.getlist('graphType')
    if data["plots"] == []: return None
    # Elevation will always be passed due to default value
    data["elevation"] = int(html_data["elevation"])

    # Empty list to store html strings of interactive and pdf forms for each graph requested
    graphs = []
    pdfs = []

    # Iterate through plot types requested and make graph for each plot
    for plot in  data["plots"]:
        print(f"User is requesting a {plot} plot for the months: {data['months']}")

        if plot == "sfcTemp":
            # Create surface temperature plot
            testPlot = SurfaceTemperaturePlot(months = data["months"])

        elif plot == "tempElev":
            # Create surface temperature plot
            testPlot = ElevationTemperature(months = data["months"], elevation=data["elevation"])

        elif plot == "pcpRate":
            # Create precipitation rate plot
            testPlot = PrecipitationRatePlot(months= data["months"])
        
        elif plot == "pcpAmnt":
            # Create precipitation amount plot
            testPlot = PrecipitationAmountPlot(months= data["months"])

        # Set the data, make the figure, and create the pdf
        testPlot.create_plot()

        # Convert figure to an html string
        graph = mpld3.fig_to_html(testPlot.fig)

        # Add the new graph to the list of graphs to be updated in the html file
        graphs.append(graph)

        # Add the new pdf of the graph
        pdfs.append(testPlot.pdf)

    # Return the list of graphs to be rendered in the html file
    return {"graphs":graphs, "pdfs":pdfs}