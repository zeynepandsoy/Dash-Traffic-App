# Import the required packages
#import Dash, HTML, Dash Core Components and Input/Output (interactivity)
from dash import Dash, Input, Output, html, dcc
# import Dash Bootsrap Components
import dash_bootstrap_components as dbc

#from multi_page_app.app import app
from app import app

#import helper functions to create the charts
import pandas as pd
import plotly.express as px
from pathlib import Path

# Define the path to excel datafile
traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

def line_chart():
    cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']
    df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)
    line_traffic = px.line(df_traffic,
                          x='Year',
                          y='traffic_volume',
                          color='weather',
                          labels={'Year': '', 'traffic_volume': 'traffic_volume over time', 'weather': ''},
                          template="simple_white"
                          )
    # Remove the x-axis labels and tick lines
    line_traffic.update_xaxes(showticklabels=False, ticklen=0)
    return line_traffic

app.layout = dbc.Container(
    [
        html.H1("Traffic app Dashboard"),
        html.H2("Observe traffic volume over time"),
        dcc.Graph(
            id='line-traffic',
            figure=line_chart
        ),
    ],
    fluid=True,
)
