# in app.py we have our Dash instance and we will apply our template within app.py 
#so that we have aconsistent sytle for each page

# when we define the instance of dash we pass in the Dashboot-bootsrap component
#LUX template in the argument

import dash
from dash import callback
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#from app import app
from apps import app1, app2

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="apps",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ]
)

app.layout = dbc.Container(
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
          dash.page_container,
      ]
)
"""
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/apps/app1", active="exact"),
                dbc.NavLink("Page 2", href="/apps/app2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/apps/app1":
        return app1
    elif pathname == "/apps/app2":
        return app2
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
"""









"""

# Navbar https://community.plotly.com/t/introducing-dash-pages-a-dash-2-x-feature-preview/57775

# Bootstrap style layout in a container
app.layout = dbc.Container(
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
          #dash.page_container,
      ]
)

#2ND NAVI CODE

#FIGURE OUT HOW TO LINK NAVI CODE TO MULTI PAGES
#add navigation bar for multipage app
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/app1"), id="app-1-link"),
        dbc.NavItem(dbc.NavLink("Page 2", href="/app2"), id="app-2-link")
    ],
    brand="Multi page app Dash Pages",
    brand_href="/",
    color="primary",
    dark=True,
)

#EVERYTHING IN EACH LAYOUT MUST BE IN A DBC CONTAINER
#change the layout to dbc container 
layout = html.Div([
	#navbar,
	html.H1('Multi-page app with Dash Pages'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])
 
3RD NAVI CODE
# Bootstrap style layout in a container
layout = dbc.Container(
 dbc.NavbarSimple(
     children=[
         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
         dbc.DropdownMenu(
              children=[
                 dbc.DropdownMenuItem("More pages", header=True),
                 dbc.DropdownMenuItem("Page 2", href="#"),
                 dbc.DropdownMenuItem("Page 3", href="#"),
             ],
             nav=True,
             in_navbar=True,
             label="More",
         ),
     ],
     brand="NavbarSimple",
     brand_href="#",
     color="primary",
     dark=True,
 )
 )

"""

if __name__ == "__main__":
    app.run_server(debug=True, port=8667)


