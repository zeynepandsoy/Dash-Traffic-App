# define routing for the app and the layout for the index page
# the routing uses a callback to define which apps to display when a user selects
# a particular URL
#Layout for overall app.py provides a kindof template for pages in the app

#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# import the seperate apps
#from multi_page_app.apps.app1 import app1
#from multi_page_app.apps.app2 import app2

#import the instance of Dash app
#from multi_page_app.app import app

# Below code is implemented from https://github.com/plotly/dash-recipes/blob/master/multi-page-app/index.py

from app import app
from apps import app1, app2

#add navigation bar for multipage app
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/app1"), id="app-1-link"),
        dbc.NavItem(dbc.NavLink("Page 2", href="/app2"), id="app-2-link")
    ],
    brand="Multi page app example",
    brand_href="/",
    color="primary",
    dark=True,
)


app.layout=html.Div([
    dcc.Location(id='url', refresh= False),
    navbar,
    html.Div(id='page-content')
])

index_layout = html.Div([
    html.P('Hello')
])

#this callback function handles the routing for the apps
@app.callback(Output('page-content', 'children'), [Input('url','pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/':
        return index_layout
    else:
        return '404 Page Not Found'
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8025)
