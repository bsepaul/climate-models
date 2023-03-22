from flask import Flask
# from flask import Flask, render_template, request
import base64
from io import BytesIO
# import json
# from temperature import TemperaturePlot
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# import geocat.viz as gv
# import cartopy.crs as ccrs
# import numpy as np
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def hello():

    # TESTING!!!!
    # Generate the figure **without using pyplot**.
    from matplotlib.figure import Figure
    fig = Figure(figsize=(10,8))
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

    # if request.method == "POST":
    #     jsonData = json.loads(request.get_json())
    #     print(jsonData["months"])
    #     testPlot = TemperaturePlot(jsonData["months"])
    #     try:
    #         testPlot.create_plot()
    #     except:
    #         print("Internal Inconsistency Error")
    #     return {
    #         'response' : 'I am the response'
    #     }
    # return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
