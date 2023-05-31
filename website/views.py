from flask import Blueprint, render_template, request
from .render import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    # When the user clicks the "Create Model" button
    if request.method == "POST":

        # Get the list of html strings, each representing one graph, using the render function (render.py)
        graphs = render(request.form)

        # Pass the list of graphs into the graph.html template
        return render_template('graphs.html', graphs=graphs)

    # If the page is just being loaded, only show home.html which has no graphs
    else:
        return render_template('home.html')
