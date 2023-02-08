# Import the required packages
#import Dash, HTML, Dash Core Components and Input/Output (interactivity)
import dash
from dash import callback
from dash import Dash, Input, Output, html, dcc
# import Dash Bootsrap Components
import dash_bootstrap_components as dbc

#from multi_page_app.app import app
#from app import app

from datetime import date

#import helper functions to create the charts
import pandas as pd
import plotly.express as px
from pathlib import Path

dash.register_page(__name__, path="/")

# Define the path to excel datafile
traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)
#print(df_traffic.head(20))


#create a new datetime column and use it to show different traffic entries based on user input on calendar

date_cols=['Year','Month','Day']

df_traffic['date'] = df_traffic[date_cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
#print(df_traffic.head(20))

df_traffic['date']=pd.to_datetime(df_traffic['date'])

#aggregate traffic volume over years
df_agg_trfc = df_traffic.groupby('date').aggregate({'traffic_volume':'mean'}) # changed this to 'Day' from 'Year'
print(df_agg_trfc.head(20))


#this app will display average traffic volume over the years and (will be added: calendar
# functionality)

# Dash components 
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df_traffic.columns.values[0:], # CHOOSE ONLY A FEW COLUMNS TO DISPLAY
                        value='holiday',  # initial value displayed when page first loads
                       clearable=False)
datepicker = dcc.DatePickerSingle(
    #id='my-date-picker-single',
    min_date_allowed=date(2012, 10, 2),
    max_date_allowed=date(2018, 9, 30),
    initial_visible_month=date(2012, 10, 2),
    date = date(2012, 10, 2) #degistir
)



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
    dbc.Row([
        dbc.Col([datepicker], width=4)
    ]),

], fluid=True)


# Callback allows components to interact
@callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Output(datepicker, 'children'),
    Input(dropdown, 'value'),
    Input(datepicker, 'date')
)

def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string
    
#include below column_name as function argument
def update_graph(column_name):  # function arguments come from the component property of the Input
    #print(column_name)
    #print(type(column_name))
    #df_agg_trfc_copy = df_agg_trfc.copy
    fig = px.line(df_traffic,  #chnage to df_agg_trfc
                  x='Year', #change
                  y='traffic_volume',
                  #labels={'Year': '', 'traffic_volume': 'traffic_volume over time'},
                  color=column_name,
                  #template="simple_white"
                  animation_frame='Year'
                  )  
    return fig, '# '+column_name  # returned objects are assigned to the component property of the Output

