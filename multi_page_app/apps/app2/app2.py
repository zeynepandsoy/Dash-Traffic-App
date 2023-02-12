import dash  # version 1.13.1
from dash import dcc
from dash import html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

dash.register_page(__name__)


traffic_data_filepath = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')

cols = ['holiday', 'weather', 'traffic_volume', 'Year', 'Month', 'Day', 'Hour', 'categorized_hour', 'categorized_weekday']

df_traffic = pd.read_excel(traffic_data_filepath, usecols=cols)


df_traffic.rename(columns={'traffic_volume': 'traffic volume', 'categorized_hour': 'categorized hour', 'categorized_weekday': 'categorized weekday'}, inplace=True)

# create a new column; traffic density, dividing each subsequent traffic volume entry by its overall mean
df_traffic['traffic density'] = df_traffic['traffic volume'] / df_traffic['traffic volume'].mean(axis=0)
#print(df_traffic.head())
#print(df_traffic[['traffic volume']].mean())


# Below code for app2 is implemented from:
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Callbacks/Pattern%20Matching%20Callbacks/dynamic_callbacks.py

layout = dbc.Container([
    dbc.Container(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    dbc.Container(id='container', children=[])
])

#layout = dbc.Container(children=[[mytitle], [mygraph], [dropdown]])

@callback(
    #state & input will be the arguments of below function, what is returned will go into the children of container(output)
    Output('container', 'children'), 
    [Input('add-chart', 'n_clicks')], #take the n_clicks of the add-chart component id (button)
    [State('container', 'children')] #take the state of component children which is Div that is empty list []
)


# 'n_clicks'of Input and 'children' of State is arguments of fuction
# when someone clicks n_clicks triggers below function
def display_graphs(n_clicks, div_children):
    # new_child variable is an html.Div with many different childrens (graph,radioitem)
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
    div_children.append(new_child) #new_child will be appended to div_children (children of state:[])
    return div_children  
#each time button is clicked another html.Div will be added in the list which goes in chrildren of cotainer (Output)
#which goes in children=[] in main layout

#DYNAMICAL CALLBACKS (Pattern Matching Callbacks)
@callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-y', 'index': MATCH}, component_property='value'), #for year
     Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'), #categorical values
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'), #numerical values
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')] 
)
#df_month = df_traffic[df_traffic['holiday'] != 'None']

#as we have 4 inputs we have 4 argument (change their names)
def update_graph(y_value, ctg_value, num_value, chart_choice):
    print(y_value)
    # make a copy of the dataframe and filter the data such that it only has different categorized hours
    dff_traffic = df_traffic[df_traffic['categorized hour'].isin(y_value)]
    print(dff_traffic.head())

    if chart_choice == 'bar':
        dff_traffic = dff_traffic.groupby([ctg_value], as_index=False)[['traffic volume','traffic density']].mean()
        
        fig = px.bar(dff_traffic, x=ctg_value, y=num_value)
        return fig
    
    elif chart_choice == 'line':
        if len(y_value) == 0:
            return {}
        else:
            dff_traffic = dff_traffic.groupby([ctg_value, 'Year'], as_index=False)[['traffic volume','traffic density']].mean()
            fig = px.line(dff_traffic, x='Year', y=num_value, color=ctg_value)
            return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff_traffic, names=ctg_value, values=num_value)
        return fig

