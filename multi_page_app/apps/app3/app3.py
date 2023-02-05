# THIS VERSION WORKS

# Import the required packages
#import Dash, HTML, Dash Core Components and Input/Output (interactivity)
from dash import Dash, Input, Output, html, dcc
# import Dash Bootsrap Components
import dash_bootstrap_components as dbc

#import helper functions to create the charts
import pandas as pd
import plotly.express as px
from pathlib import Path

# Define the path to excel datafile
traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)
df_traffic.head()

line_traffic = px.line(df_traffic,
                          x='Year',
                          y='traffic_volume',
                          color='weather',
                          labels={'Year': '', 'traffic_volume': 'traffic_volume over time', 'weather': ''},
                          template="simple_white"
                          )

app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        },
    ],
)

app.layout = dbc.Container(
    [
        html.H1("Traffic app Dashboard"),
        html.H2("Observe traffic volume over time"),
        dcc.Graph(
            id='line-traffic',
            figure=line_traffic
        ),
    ],
    fluid=True,
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8058)

# when i try to run the app in terminal saying 'python multi_page_app/app3.py'
# it returns error stating no such file 