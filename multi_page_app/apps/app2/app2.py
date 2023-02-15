#import necessary packages
import dash  
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
#'ALL', 'MATCH' and 'ALLSMALLER' are pattern matching (dynamical) callbacks
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER

#import helper functions for graphs
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

# Define the path to the page
dash.register_page(__name__)


# Define the path to excel datafile
traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)

# Rename columns for visual aesthetics
df_traffic.rename(columns={'traffic_volume': 'traffic volume', 'categorized_hour': 'categorized hour', 'categorized_weekday': 'categorized weekday'}, inplace=True)

# Dividing each subsequent traffic volume entry by its overall mean, create a new 'traffic density' column
df_traffic['traffic density'] = df_traffic['traffic volume'] / df_traffic['traffic volume'].mean(axis=0)
#print(df_traffic[['traffic volume']].mean())
 

# Below code for app2 is adapted from code written by user 'Coding-with-Adam' on Github
# Code Available at: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Callbacks/Pattern%20Matching%20Callbacks/dynamic_callbacks.py

# initial layout only has an html button and empty container
layout = dbc.Container([
    dbc.Container(children=[
        html.H2('Compare descriptive/categorical features impacts on traffic volume'),
        html.H3('Recommended for reseachers'),
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    dbc.Container(id='container', children=[])
])


@callback(
    Output('container', 'children'), 
    [Input('add-chart', 'n_clicks')], 
    [State('container', 'children')] 
)


def display_graphs(n_clicks, div_children):
    """
    This function  generates a new figure for every click on 'add chart' 
    (Appends 'new_child' to 'div_children' for every click)
    
    Parameters
    ----------
    n_clicks: int
    component property of the Input with component id: 'add-chart' (number of clicks to 'add-chart')
    div_children: list
    component property of the State with component id: 'children' which is Div that is initially []

    Note: only 'n_clicks'(Input) triggers the function 

    Returns
    ----------
    div_children: list
    each time button is clicked another html.Div will be added in the list which goes in the 'children'
    of container (Output), which goes in children=[] in main layout   

    """
    # new_child variable is an html.Div with many different childrens
    new_child = dbc.Container(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Line Chart', 'value': 'line'},
                         {'label': 'Pie Chart', 'value': 'pie'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-y',
                    'index': n_clicks
                },
                options=[{'label': y, 'value': y} for y in np.sort(df_traffic['categorized hour'].unique())],
                multi=True,
                value=["Morning", "Afternoon"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['categorized hour', 'weather', 'categorized weekday','holiday']],
                value='categorized hour',  
                clearable=False
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                options=[{'label': n, 'value': n} for n in ['traffic volume', 'traffic density']],
                value='traffic volume',
                clearable=False
            )
        ]
    )
    # Append 'new_child' to 'div_children' (children of state:[])
    div_children.append(new_child) 
    return div_children  



#DYNAMICAL CALLBACKS (Pattern Matching Callbacks)
@callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-y', 'index': MATCH}, component_property='value'), 
     Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'), 
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'), 
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')] 
)


def update_graph(y_value, ctg_value, num_value, chart_choice):
    """
    This function generates the 3 different types of plots (line, bar, pie) based multiple user inputs

    Parameters
    ----------
    (as there are 4 inputs, the function has 4 arguments)

    chart_choice: str
    'value' of 'dynamic-choice' (radioitem of chart choice)

    num_value: str
    'value' of 'dynamic-dpn-num' (dropdown of numerical traffic values)

    ctg_value: str
    'value' of 'dynamic-dpn-ctg' (dropdown of categorical features)

    y_value: list
    'value' of 'dynamic-dpn-y' (dropdown of unique catgeorized hour values)

    Note: To see a clear comparison between different holidays, as categorized hour desciption,
    'night' must be selected as traffic volumes for holiday days are recorded only at 'night'
    
    Returns
    ----------
    fig: Figure
    'figure' with 'dynamic-graph'

    """
    print(y_value)
    
    # copy & filter the data such that it only has different categorized hours
    dff_traffic = df_traffic[df_traffic['categorized hour'].isin(y_value)]
    #print(dff_traffic.head())

    if chart_choice == 'bar':
        dff_traffic = dff_traffic.groupby([ctg_value], as_index=False)[['traffic volume','traffic density']].mean()
        fig = px.bar(dff_traffic, x=ctg_value, y=num_value)
        # Increase data-ink ratio by removing background colour and removing legends)
        fig.update_layout(showlegend=False, paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)')
        return fig
    
    elif chart_choice == 'line':
        if len(y_value) == 0:
            return {}
        else:
            dff_traffic = dff_traffic.groupby([ctg_value, 'Year'], as_index=False)[['traffic volume','traffic density']].mean()
            fig = px.line(dff_traffic, x='Year', y=num_value, color=ctg_value)
            fig.update_layout(showlegend=False, paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)')
            return fig
        
    elif chart_choice == 'pie':
        fig = px.pie(dff_traffic, names=ctg_value, values=num_value)
        fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)')
        return fig

