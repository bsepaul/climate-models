from temperature import TemperaturePlot
from precipitation import PrecipitationPlot
import mpld3

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

    # html_data format that cannot be easily parsed
    # ImmutableMultiDict([('sfcTemp', 'on'), ('pcpRate', 'on'), ('pcpAmnt', 'on'), ('04', 'on'), ('05', 'on'), ('06', 'on')])
    
    data = parse(html_data)

    # data format that can be easily parsed
    # {'plots': ['sfcTemp', 'pcpRate', 'pcpAmnt'], 'months': ['04', '05', '06']}

    # Empty list to store html strings for each graph requested
    graphs = []

    # Iterate through plot types requested and make graph for each plot
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

        # Convert figure to an html string
        graph = mpld3.fig_to_html(fig)

        # Add the new graph to the list of graphs to be updated in the html file
        graphs.append(graph)

    # Return the list of graphs to be rendered in the html file
    return graphs