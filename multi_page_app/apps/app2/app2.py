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

date_cols=['Year','Month','Day']

df_traffic['date'] = df_traffic[date_cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
#print(df_traffic.head(10))

df_traffic['date']=pd.to_datetime(df_traffic['date'])

df_traffic = df_traffic.reindex(['Year', 'Month', 'Day', 'Hour','date','holiday','weather','categorized_hour','categorized_weekday', 'traffic_volume'], axis=1)
print(df_traffic.head())


mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df_traffic.columns.values[0:5],
                        value='date',  # initial value displayed when page first loads
                        clearable=False)


#layout = dbc.Container(children=[[mytitle], [mygraph], [dropdown]])


layout = dbc.Container([
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