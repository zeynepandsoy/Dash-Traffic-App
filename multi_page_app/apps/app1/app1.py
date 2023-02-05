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
#---------
# Dash app
#---------

"""
app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        },
    ],
)
"""



"""
if __name__ == '__main__':
    app.run_server(debug=True, port=8058)
"""

"""
# Creates the Dash app
app = Dash(__name__, 
external_stylesheets=[dbc.themes.BOOTSTRAP],
meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Holiday', 'Weather', 'Day of the Week','Time of the Day'],
                        value='Holiday',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
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


#app.layout = dbc.Container(children=[
    # HTML layout elements 
#    html.H1(children='Hello, World!'),
#    html.H1(children='Heading with Bootsrap "display-1" style', className="display-1"),
#    html.P('My first app')

#])
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


    def line_chart_sports():
    
    #Creates a line chart showing change in the number of sports in the summer and winter paralympics over time.
    #:return: Plotly Express line chart
    
    cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']
    df_traffic = pd.read_csv(traffic_data_filepath, usecols=cols)

    # px line charts https://plotly.com/python/line-charts/
    # Styling figures with px https://plotly.com/python/styling-plotly-express/
    line_events = px.line(df_traffic,
                          x='YEAR',
                          y='EVENTS',
                          color='TYPE',
                          text='YEAR',
                          title='Have the number of events changed over time?',
                          labels={'YEAR': '', 'EVENTS': 'Number of events', 'TYPE': ''},
                          template="simple_white"
                          )

    # Add an annotation https://plotly.com/python/text-and-annotations/
    line_events.add_annotation(
        text='Event in multiple locations, Stoke Mandeville and New York',
        x='1984',
        y=975,
        showarrow=True,
        arrowhead=2
    )

    # Remove the x-axis labels and tick lines
    line_events.update_xaxes(showticklabels=False, ticklen=0)

    return line_events
"""