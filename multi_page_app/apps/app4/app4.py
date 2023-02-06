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


# This app will display 2 different plots based on user input (one will be later
# changed to piechart) user clicks on either holiday or weather from the dropdown
#menu and the graph and title changes 

app = Dash(__name__, 
external_stylesheets=[dbc.themes.BOOTSTRAP],
meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Holiday', 'Weather'],
                        value='Holiday',  # initial value displayed when page first loads
                        clearable=False)

#add above 'Day of the Week','Time of the Day'

# Customize your own Layout
app.layout = dbc.Container([mytitle],[mygraph],[dropdown])
  
# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Output(mytitle, component_property='children'),
    Input(dropdown, component_property='value')
)

def update_graph(user_input):  # function arguments come from the component property of the Input
    if user_input == 'Weather':
         # Aggregate traffic volume hour description in a new dataframe 
         df_wthr = df_traffic.groupby(df_traffic['holiday']).aggregate({'traffic_volume':'mean'})
         fig = px.bar(data_frame=df_wthr, x=df_wthr.index, y="traffic_volume")

    elif user_input == 'Holiday':
        df_hldy = df_traffic[df_traffic['holiday'] != 'None']
        df_trfc_hldy = df_hldy.groupby(df_hldy['holiday']).aggregate({'traffic_volume':'mean'})
        fig = px.bar(data_frame=df_trfc_hldy, x=df_trfc_hldy.index, y="traffic_volume")

    return fig  # returned objects are assigned to the component property of the Output

if __name__ == '__main__':
    app.run_server(debug=True)