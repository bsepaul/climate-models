from flask import Flask, render_template, request
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure
from temperature import TemperaturePlot

# FLASK APPLICATION
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():

    ##############
    #### TEST ####
    ##############

    # Create figure (this is just a test figure)
    fig = Figure(figsize=(10, 8))
    ax = fig.subplots()
    ax.plot([1, 2])

    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Open the html file and read in the lines
    with open('templates/home.html', 'r', encoding='utf-8') as file:
        html_file = file.readlines()

    # Replace line 38 (the 37th line) with the figure
    html_file[37] = f"<img src='data:image/png;base64,{data}'/>"

    # Write the updated html back to the original file
    with open('templates/home.html', 'w', encoding='utf-8') as file:
        file.writelines(html_file)

    ##############
    #### REAL ####
    ##############

    # When the user clicks the "Create Model" button
    if request.method == "POST":
        jsonData = json.loads(request.get_json())
        for plot in jsonData["plot"]:
            print("User is requesting a {} plot for the months: {}".format(
                plot, jsonData["months"]))

            # Create plot
            testPlot = TemperaturePlot(jsonData["months"])

            # Set the data
            testPlot.set_data()

            # LINE 61 IS CAUSING ERROR ON MAC OS
            # # Get the figure
            # fig = testPlot.make_fig()
            # # Save it to a temporary buffer.
            # buf = BytesIO()
            # fig.savefig(buf, format="png")
            # # Embed the result in the html output.
            # data = base64.b64encode(buf.getbuffer()).decode("ascii")
            # graph = f"<img src='data:image/png;base64,{data}'/>"

            # with open('test.html', 'w', encoding='utf-8') as file:
            #     file.writelines(graph)

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
