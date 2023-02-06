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

#aggregate traffic volume over years
df_agg_trfc = df_traffic.groupby('Year').aggregate({'traffic_volume':'mean'})
df_agg_trfc.head()

#this app will display average traffic volume over the years and (will be added: calendar
# functionality)

app = Dash(__name__,
    external_stylesheets=[dbc.themes.LUX])
    #meta_tags=[
    #    {
    #        "name": "viewport",
    #        "content": "width=device-width, initial-scale=1"
    #    },
    #],

mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df_traffic.columns.values[0:],
                        value='holiday',  # initial value displayed when page first loads
                       clearable=False)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  # function arguments come from the component property of the Input
    #print(column_name)
    #print(type(column_name))
    df_agg_trfc_copy = df_agg_trfc.copy
    fig = px.line(df_agg_trfc,
                  x=df_agg_trfc.index,
                  y='traffic_volume',
                  labels={'Year': '', 'traffic_volume': 'traffic_volume over time'},
                  color=column_name,
                  #template="simple_white"
                  #animation_frame='Year'
                  )
    #graph doesnt work

    return fig, '# '+column_name  # returned objects are assigned to the component property of the Output


if __name__ == '__main__':
    app.run_server(debug=True, port=8059)

# when i try to run the app in terminal saying 'python multi_page_app/app3.py'
# it returns error stating no such file 

"""
line_traffic = px.line(df_traffic,
                          x='Year',
                          y='traffic_volume',
                          #color='weather',
                          labels={'Year': '', 'traffic_volume': 'traffic_volume over time', 'weather': ''},
                          template="simple_white"
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
"""