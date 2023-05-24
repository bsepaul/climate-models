from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure
from temperature import TemperaturePlot
from precipitation import PrecipitationPlot
from .render import *
import time
import mpld3
import numpy as np
import matplotlib.pyplot as plt


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    ##############
    #### TEST ####
    ##############

    # # Create figure (this is just a test figure)
    # fig = Figure(figsize=(10, 8))
    # ax = fig.subplots()
    # ax.plot([1, 2])

    # # Save it to a temporary buffer
    # buf = BytesIO()
    # fig.savefig(buf, format="png")

    # # Embed the result in the html output
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # # Open the html file and read in the lines
    # with open('templates/home.html', 'r', encoding='utf-8') as file:
    #     html_file = file.readlines()

    # # Replace line 38 (the 37th line) with the figure
    # html_file[37] = f"<img src='data:image/png;base64,{data}'/>"

    # # Write the updated html back to the original file
    # with open('templates/home.html', 'w', encoding='utf-8') as file:
    #     file.writelines(html_file)

    ##############
    #### REAL ####
    ##############
    graphs = "<div/>"
    # return render_template('home.html')
    # When the user clicks the "Create Model" button
    if request.method == "POST":
        print(request.form)
        # jsonData = json.loads(request.get_json())
        graphs = render(request.form)
        # return render_template('home.html', graphs="Graphs!")
        return render_template('graphs.html', graphs=graphs)
        # return render_template('home.html', async_mode=socketio.async_mode)
    else:
        return render_template('home.html')

# @views.route('/result', methods=['GET', 'POST'])
# def result():
#     return "<div>Hello</div>"
#     # When the user clicks the "Create Model" button
#     print("Result!")
#     if request.method == "POST":
#         jsonData = json.loads(request.get_json())
#         # graphs = render(jsonData)
#         return render_template('home.html', graphs="Result!")
#         # return render_template('home.html', async_mode=socketio.async_mode)
#     else :
#         return render_template('home.html', graphs="Result!!")
