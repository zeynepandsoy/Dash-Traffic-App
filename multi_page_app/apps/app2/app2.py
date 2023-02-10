# Copied from the Dash documetation sample code at https://github.com/plotly/dash-recipes/tree/master/multi-page-app
#DOESNT WORK
import dash
from dash import callback
from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc
#from multi_page_app.app import app
#from app import app
#import helper functions to create the charts
import pandas as pd
import plotly.express as px
from pathlib import Path

dash.register_page(__name__)


traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)

df_traffic = df_traffic.reindex(['holiday','weather','categorized_hour','categorized_weekday', 'Year', 'Month', 'Day', 'Hour', 'traffic_volume'], axis=1)
#print(df_traffic.head())


mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df_traffic.columns.values[0:4],
                        value='categorized_hour',  # initial value displayed when page first loads
                        clearable=False)


#layout = dbc.Container(children=[[mytitle], [mygraph], [dropdown]])

layout = dbc.Container([
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
@callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)


def update_graph(user_input):  # function arguments come from the component property of the Input
    if user_input == 'weather':
         # Aggregate traffic volume hour description in a new dataframe 
         df_wthr = df_traffic.groupby(df_traffic['weather']).aggregate({'traffic_volume':'mean'})
         fig = px.bar(data_frame=df_wthr, x=df_wthr.index, y="traffic_volume")

    elif user_input == 'holiday':
        df_hldy = df_traffic[df_traffic['holiday'] != 'None']
        df_trfc_hldy = df_hldy.groupby(df_hldy['holiday']).aggregate({'traffic_volume':'mean'})
        fig = px.bar(data_frame=df_trfc_hldy, x=df_trfc_hldy.index, y="traffic_volume")

    elif user_input == 'categorized_hour':
        df_hour = df_traffic.groupby(df_traffic['categorized_hour']).aggregate({'traffic_volume':'mean'})
        #print(df_hour.head())
        fig = px.pie(data_frame=df_hour, values='traffic_volume', names=df_hour.index)

    elif user_input == 'categorized_weekday':
        df_weekday= df_traffic.groupby(df_traffic['categorized_weekday']).aggregate({'traffic_volume':'mean'})
        fig = px.pie(data_frame=df_weekday, values='traffic_volume', names=df_weekday.index)
    

    return fig , '# '+user_input  # returned objects are assigned to the component property of the Output



"""

layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Fruit Selector'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in [
                'Apple', 'Banana', 'Coconut', 'Date'
            ]
        ]
    ),
    html.Div(id='app-2-display-value')
])


@callback(Output('app-2-display-value', 'children'), Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)
"""