from temperature_surface import TemperatureSurfacePlot
from temperature_elevation import TemperatureElevation
from precipitation_amount import PrecipitationAmountPlot
from precipitation_rate import PrecipitationRatePlot
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
    data["color"] = html_data["color"]

    # If user left a box blank, set the value to its default value
    data["min_longitude"] = int(html_data["min_longitude"]) if html_data["min_longitude"] != '' else -180
    data["max_longitude"] = int(html_data["max_longitude"]) if html_data["max_longitude"] != '' else 180
    data["min_latitude"]  = int(html_data["min_latitude"])  if html_data["min_latitude"]  != '' else -90
    data["max_latitude"]  = int(html_data["max_latitude"])  if html_data["max_latitude"]  != '' else 90

    # Elevation will always be passed due to default value
    data["elevation"] = int(html_data["elevation"])

    # Empty list to store html strings of interactive and pdf forms for each graph requested
    graphs = []
    pdfs = []
    print(f"\nparsed data:\n{data}\n")

    # Iterate through plot types requested and make graph for each plot
    for plot in  data["plots"]:
        print(f"User is requesting a {plot} plot for the months: {data['months']}")

        if plot == "tempSfc":
            # Create surface temperature plot
            testPlot = TemperatureSurfacePlot(
                months = data["months"], 
                time_periods = data["timePeriods"], 
                color = data["color"], 
                min_longitude=data["min_longitude"], 
                max_longitude=data["max_longitude"], 
                min_latitude=data["min_latitude"], 
                max_latitude=data["max_latitude"], 
                central_longitude=0)

        elif plot == "tempElev":
            # Create elevation temperature plot
            testPlot = TemperatureElevation(
                months = data["months"], 
                time_periods = data["timePeriods"], 
                elevation=data["elevation"], 
                color = data["color"], 
                min_longitude=data["min_longitude"], 
                max_longitude=data["max_longitude"], 
                min_latitude=data["min_latitude"], 
                max_latitude=data["max_latitude"], 
                central_longitude=0)

        elif plot == "pcpRate":
            # Create precipitation rate plot
            testPlot = PrecipitationRatePlot(
                months= data["months"], 
                time_periods = data["timePeriods"], 
                color = data["color"], 
                min_longitude=data["min_longitude"], 
                max_longitude=data["max_longitude"], 
                min_latitude=data["min_latitude"], 
                max_latitude=data["max_latitude"], 
                central_longitude=0)
        
        elif plot == "pcpAmnt":
            # Create precipitation amount plot
            testPlot = PrecipitationAmountPlot(
                months= data["months"], 
                time_periods = data["timePeriods"], 
                color = data["color"], 
                min_longitude=data["min_longitude"], 
                max_longitude=data["max_longitude"], 
                min_latitude=data["min_latitude"], 
                max_latitude=data["max_latitude"], 
                central_longitude=0)

        # Set the data, make the figure, and create the pdf
        testPlot.create_plot()

    # Send a response containing the converted fig to html string, the png version of the graph, and the pdf version of the graph
    return {"graph":(mpld3.fig_to_html(testPlot.fig)), "png":(testPlot.png), "pdf":(testPlot.pdf)}