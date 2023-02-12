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

dash.register_page(__name__) #path='/'

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

#2nd app inputs
df_traffic_app2 = df_traffic.reindex(['Year', 'Month', 'Day', 'Hour','date','holiday','weather','categorized_hour','categorized_weekday', 'traffic_volume'], axis=1)
#print(df_traffic_app2.head())

#dash components for app2
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df_traffic_app2.columns.values[0:5],
                        value='date',  # initial value displayed when page first loads
                        clearable=False)


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

below is example in dbc container

layout = dbc.Container([
    html.H1('Dash Tabs component demo'),
    dbc.Tabs(
    [
        dbc.Tab(label="Scatter", tab_id="scatter"),
        dbc.Tab(label="Histograms", tab_id="histogram"),
    ],
"""
#try to initialize 1st tab to open when app1 is clicked
layout = dbc.Container([
    html.H1('Traffic Analysis App'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[ 
        dcc.Tab(label='Tab One (date boxplot)', value='tab-1-boxplot'),
        dcc.Tab(label='Tab Two (date line chart)', value='tab-2-linechart'),
    ]),
    html.Div(id='tabs-content-example-graph')
])

@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))

def render_content(tab):
    if tab == 'tab-1-boxplot':
        return html.Div([
            html.H3("Box Plot of Hourly I-94 ATR 301 westbound traffic volume over different date time features"),
            html.H2("Observe traffic volume over time"),
            html.P("x-axis:"),
            dcc.Checklist(
                id='x-axis', 
                options=['Year', 'Month', 'Day', 'Hour'],
                value=['Year'], 
                inline=True
            ),
            dcc.RadioItems(
                id = 'distribution-plot-choice',
                options=[{'label': 'Box Plot', 'value': 'box'},
                         {'label': 'Violing PLot', 'value': 'violin'}],
                value = 'box'
        
            ),
            dcc.Graph(id="tab2-plot-figure",figure={})   
            #dcc.Graph(id="box-plot-figure"),
        ])


    elif tab == 'tab-2-linechart':
        return html.Div([
            html.H3("Line Chart of Hourly I-94 ATR 301 westbound traffic volume over different date time features"),
            dbc.Row([
                dbc.Col([mytitle], width=6)
            ], justify='center'),
            dbc.Row([
               dbc.Col([mygraph], width=12)
            ]),
            dbc.Row([
                dbc.Col([dropdown], width=6)
            ], justify='center'),

]) #, fluid=True
            
       
# Callback allows components to interact
#1st callback refers to tab1
@callback(
    Output("tab2-plot-figure",'figure'), 
    Input("x-axis", 'value'),
    Input("distribution-plot-choice",'value')
   )

#1st function generates the interactive boxplot in tab 1
#def generate_chart(x):  # function arguments come from the component property of the Input
#    #print(x)
#    #df_year = df_traffic.groupby(df_traffic['Year']).aggregate({'traffic_volume':'mean'})
#    fig = px.box(df_traffic, x=x, y="traffic_volume")
#    return fig

def generate_chart(x,user_choice):  # function arguments come from the component property of the Input
        #print(type(user_choice))
        if user_choice == 'box':
            #df_year = df_traffic.groupby(df_traffic['Year']).aggregate({'traffic_volume':'mean'})
            fig = px.box(df_traffic, x=x, y="traffic_volume")
            

        elif user_choice == 'violin':
            fig = px.violin(df_traffic, x=x, y='traffic_volume', box=True)
                         #points="all"
                         #labels={'Year': '', 'traffic_volume': 'average traffic volume'},
                         #template="simple_white"
        return fig  #'# '+user_choice 


# Callback allows components to interact
# 2nd callback refers to tab 2
@callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
#2nd function generates the aggragate traffic volume line plot based on user choice from different date features presented in the dropdown
def update_graph(user_input):  # function arguments come from the component property of the Input
    if user_input == 'Year':
         # Aggregate traffic volume hour description in a new dataframe 
         df_year = df_traffic.groupby(df_traffic['Year']).aggregate({'traffic_volume':'mean'})
         fig = px.line(df_year,
                         x= df_year.index,
                         y='traffic_volume',
                         labels={'Year': '', 'traffic_volume': 'average traffic volume'},
                         template="simple_white"
                         )

    elif user_input == 'Month':
        df_month = df_traffic.groupby(df_traffic['Month']).aggregate({'traffic_volume':'mean'})
        fig = px.line(df_month,
                    x= df_month.index,
                    y='traffic_volume',
                    labels={'Month': '', 'traffic_volume': 'average traffic volume'},
                    template="simple_white"
                    )
        

    elif user_input == 'Day':
        df_day= df_traffic.groupby(df_traffic['Day']).aggregate({'traffic_volume':'mean'})
        #print(df_hour.head())
        fig = px.line(df_day,
                    x= df_day.index,
                    y='traffic_volume',
                    labels={'Day': '', 'traffic_volume': 'average traffic volume'},
                    template="simple_white"
                    )
    elif user_input == 'Hour':
        df_hour= df_traffic.groupby(df_traffic['Hour']).aggregate({'traffic_volume':'mean'})
        fig = px.line(df_hour,
                    x= df_hour.index,
                    y='traffic_volume',
                    labels={'Hour': '', 'traffic_volume': 'average traffic volume'},
                    template="simple_white"
                    )
    elif user_input == 'date':
        df_date= df_traffic.groupby(df_traffic['date']).aggregate({'traffic_volume':'mean'})
        fig = px.line(df_date,
                    x= df_date.index,
                    y='traffic_volume',
                    labels={'date': '', 'traffic_volume': 'average traffic volume'},
                    template="simple_white"
                    )
    

    return fig , '# '+user_input  # returned objects are assigned to the component property of the Output

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

not working
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