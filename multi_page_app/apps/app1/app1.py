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

dash.register_page(__name__, path='/')

# Define the path to excel datafile
traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)
#print(df_traffic.head(20))


#create a new datetime column and use it to show different traffic entries based on user input on calendar

date_cols=['Year','Month','Day']

df_traffic['date'] = df_traffic[date_cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
#print(df_traffic.head(10))

df_traffic['date']=pd.to_datetime(df_traffic['date'])

#aggregate traffic volume over years
df_agg_trfc = df_traffic.groupby('date').aggregate({'traffic_volume':'mean'}) # changed this to 'Day' from 'Year'
#print(df_agg_trfc.head(10))


#this app will display average traffic volume over the years and (will be added: calendar
# functionality)

# Dash components 


#graph should display average traffic volumes based on date (working code based on year in docs) try to add animation
#add a date picker when a user enters/submits a date show its max and min values

"""
datepicker = dcc.DatePickerSingle(
    id='my-date-picker-single',
    min_date_allowed=date(2012, 10, 2),
    max_date_allowed=date(2018, 9, 30),
    initial_visible_month=date(2012, 10, 2),
    date = date(2012, 10, 2) #degistir
)
"""


#code adapted from https://plotly.com/python/box-plots/#box-plots-in-dash

layout = dbc.Container(
     [
            dbc.Navbar(
            [
                dbc.NavItem(
                    [
                        dbc.NavLink(
                            page["name"],
                            href=(page["relative_path"]),
                            className="nav-link",
                        )
                        for page in dash.page_registry.values()
                    ],
                    className="nav-item",
                ),
            ],
            className="navbar navbar-dark bg-primary",
        ),
        #  dash.page_container,
    html.H4("Box Plot of Hourly I-94 ATR 301 westbound traffic volume over different date time features"),
    html.H2("Observe traffic volume over time"),
    html.P("x-axis:"),
    dcc.Checklist(
        id='x-axis', 
        options=['Year', 'Month', 'Day', 'Hour'],
        value=['Year'], 
        inline=True
    ),
    #datepicker,
    dcc.Graph(id="graph"),
])

# Callback allows components to interact
@callback(
    Output("graph", "figure"), 
    #Output("my-date-picker-single", 'children'),
    Input("x-axis", "value"),
    #Input("my-date-picker-single", 'date')
   )

def generate_chart(x):  # function arguments come from the component property of the Input
    #print(x)
    #df_year = df_traffic.groupby(df_traffic['Year']).aggregate({'traffic_volume':'mean'})
    fig = px.box(df_traffic, x=x, y="traffic_volume")
    return fig

"""
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string
"""

"""
line_traffic = px.line(df_agg_trfc,
                         x= df_agg_trfc.index,
                         y='traffic_volume',
                         labels={'Year': '', 'traffic_volume': 'average traffic volume'},
                         template="simple_white"
                         )

box_traffic = px.violin(df_traffic,
                         x='Month',
                         y='traffic_volume',
                         box=True, # draw box plot inside the violin
                         #points="all"
                         #labels={'Year': '', 'traffic_volume': 'average traffic volume'},
                         #template="simple_white"
                         )


layout = dbc.Container(
   [
       html.H1("Traffic app Dashboard"),
       html.H2("Observe traffic volume over time"),
       dcc.Graph(
           id='box-traffic',
           figure=box_traffic
       ),
   ],
   fluid=True,
)
"""