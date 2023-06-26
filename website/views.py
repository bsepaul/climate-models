from flask import Blueprint, render_template, request
from .render import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    # When the user clicks the "Create Model" button
    if request.method == "POST":

        # Get the list of html strings, each representing one graph, using the render function (render.py)
        renders = render(request.form)

        # if user did not select a graph type or any months don't render the graph
        if renders == None:
            return render_template('home.html')

        # Pass the list of graphs into the graph.html template
        return render_template('graphs.html', renders=zip(renders["graphs"], renders["pdfs"]))

    # If the page is just being loaded, only show home.html which has no graphs
    else:
        return render_template('home.html')

@views.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')