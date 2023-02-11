# in app.py we have our Dash instance and we will apply our template within app.py 
#so that we have aconsistent sytle for each page

# when we define the instance of dash we pass in the Dashboot-bootsrap component
#LUX template in the argument

import dash
from dash import callback
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

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
"""
tab code
app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='1', value='tab-1'),
        dcc.Tab(label='2', value='tab-2'),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='tabs-content-props')
])

@app.callback(Output('tabs-content-props', 'children'),
              Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])


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


