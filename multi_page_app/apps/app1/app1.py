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

dash.register_page(__name__) 

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

#dash components for tab2
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


tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

layout = dbc.Container([
    html.H2('Impact of different date features on traffic volumes'),
    html.H3('Recommended for general public'),
    dbc.Tabs(id="tabs-example-graph", active_tab='tab-1-boxplot', children=[ 
        dbc.Tab(label='Distribution Plot over date features', tab_id='tab-1-boxplot',style=tab_style),
        dbc.Tab(label='Line Chart over date features ', tab_id='tab-2-linechart',style=tab_style),
    ]),
    dbc.Container(id='tabs-content-example-graph') 
])

@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'active_tab')) #active_tab was value


def render_content(tab):
    if tab == 'tab-1-boxplot':
        return dbc.Container([
            html.H3("Distribution Plot of traffic volumes over different date time features"),
            html.P("Choose x-axis and type of distribution plot:"),
            dcc.Checklist(
                id='x-axis', 
                options=['Year', 'Month', 'Day', 'Hour'],
                value=['Year'], 
                inline=True
            ),
            dcc.RadioItems(
                id = 'distribution-plot-choice',
                options=[{'label': 'Box Plot', 'value': 'box'},
                         {'label': 'Violing Plot', 'value': 'violin'}],
                value = 'box'
        
            ),
            dcc.Graph(id="tab2-plot-figure",figure={})   
        ], fluid=True)


    elif tab == 'tab-2-linechart':
        return dbc.Container([
            html.H3("Line Chart of traffic volumes over different date time features"),
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
#1st callback refers to tab1
@callback(
    Output("tab2-plot-figure",'figure'), 
    Input("x-axis", 'value'),  # user input for x-axis selected from dropdown menu
    Input("distribution-plot-choice",'value')  # user input of distribution plot type selected from RadioItem
   )


#1st function generates the interactive box and violin plots in tab 1
#code adapted from https://plotly.com/python/box-plots/#box-plots-in-dash

def generate_chart(x,user_choice):  # function arguments come from the component properties of the Inputs
        #print(type(user_choice))
        if user_choice == 'box':
            fig = px.box(df_traffic, 
                         x=x, 
                         y="traffic_volume",
                         labels={'traffic_volume': 'traffic volume'})
            
        elif user_choice == 'violin':
            fig = px.violin(df_traffic, 
                            x=x, 
                            y='traffic_volume',
                            labels={'traffic_volume': 'traffic volume'},
                            box=True)

         # remove legends and backgorund color of the figures               
        fig.update_layout(showlegend=False, paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)' )
        return fig # '# '+user_choice 


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
    # update figure layout such that axis lines are hidden
    fig.update_xaxes(showline=False)
    fig.update_yaxes(showline=False) 
    return fig , '# '+user_input  # returned objects are assigned to the component property of the Output


