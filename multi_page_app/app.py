# in app.py we have our Dash instance and we will apply our template within app.py 
#so that we have aconsistent sytle for each page

# when we define the instance of dash we pass in the Dashboot-bootsrap component
#LUX template in the argument

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])
server = app.server

