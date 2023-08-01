from surface_temperature import SurfaceTemperaturePlot
from precipitation_amount import PrecipitationAmountPlot
from precipitation_rate import PrecipitationRatePlot
from temperature_elevation import ElevationTemperature
import mpld3

# render the graphs into html strings
def render(html_data):

    print(f"\nhtml data:\n{html_data}\n")

    # create an empty dictionary to store values selected by the user in the html form
    data = {}

    # Attempt to extract user's selections from the html data

    # If user didn't select a graph type, return None
    data["graphType"] = html_data.getlist('graphType')
    if data["graphType"] == []: return None

    # If the user didn't select either single or compare time periods, return None
    if data["graphType"][0] == 'compare':
        data["timePeriods"] = html_data.getlist('compareTimePeriod')
    elif data["graphType"][0] == 'single':
        data["timePeriods"] = html_data.getlist('singleTimePeriod')
    else:
        return None

    # If user didn't select any months, return None
    data["months"] = html_data.getlist('month')
    if data["months"] == []: return None

    # If user didn't select any plot types, return None
    data["plots"]  = html_data.getlist('graphVariable')
    if data["plots"] == []: return None

    # Color will always be passed due to default value
    data["color"] = html_data["color-"+html_data['graphVariable']]

    # Elevation will always be passed due to default value
    data["elevation"] = int(html_data["elevation"])

    # Empty list to store html strings of interactive and pdf forms for each graph requested
    graphs = []
    pdfs = []
    print(f"\nparsed data:\n{data}\n")

    # Iterate through plot types requested and make graph for each plot
    for plot in  data["plots"]:
        print(f"User is requesting a {plot} plot for the months: {data['months']}")

        if plot == "sfcTemp":
            # Create surface temperature plot
            testPlot = SurfaceTemperaturePlot(months = data["months"], time_periods = data["timePeriods"], color = data["color"])

        elif plot == "tempElev":
            # Create surface temperature plot
            testPlot = ElevationTemperature(months = data["months"], time_periods = data["timePeriods"], color = data["color"], elevation=data["elevation"])

        elif plot == "pcpRate":
            # Create precipitation rate plot
            testPlot = PrecipitationRatePlot(months= data["months"], time_periods = data["timePeriods"], color = data["color"])
        
        elif plot == "pcpAmnt":
            # Create precipitation amount plot
            testPlot = PrecipitationAmountPlot(months= data["months"], time_periods = data["timePeriods"], color = data["color"])

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