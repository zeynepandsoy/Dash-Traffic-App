# Import the required packages
#import Dash, HTML, Dash Core Components and Input/Output (interactivity)
from dash import Dash, Input, Output, html, dcc
# import Dash Bootsrap Components
import dash_bootstrap_components as dbc

#import helper functions to create the charts
import pandas as pd
import plotly.express as px
#from pathlib import Path

# Creates the Dash app
app = Dash(__name__, 
external_stylesheets=[dbc.themes.BOOTSTRAP],
meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

app.layout = dbc.Container(children=[
    # HTML layout elements 
    html.H1(children='Hello, World!'),
    html.H1(children='Heading with Bootsrap "display-1" style', className="display-1"),
    html.P('My first app')

])

# Creates the HTML page layout and adds it to the app. This uses dash.html package to add HTML components.
#app.layout = html.Div(
    # The first element is the html.Div. The 'child' elements of the Div are those elements that are inside the Div. In this case a H1 heading.
#    children=[
        # The 'children' of the H1 element in this case is the content to be displayed. You can also ommit the keyword as shown in the P example.
#        html.H1(children='Hello, World!'),
#        html.P('My first app'),
#        ]
#)


if __name__ == '__main__':
    app.run_server(debug=True)