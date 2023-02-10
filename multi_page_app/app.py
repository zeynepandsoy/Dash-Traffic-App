# in app.py we have our Dash instance and we will apply our template within app.py 
#so that we have aconsistent sytle for each page

# when we define the instance of dash we pass in the Dashboot-bootsrap component
#LUX template in the argument

import dash
from dash import callback
from dash import Dash, html, dcc

import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="apps",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
# Navbar https://community.plotly.com/t/introducing-dash-pages-a-dash-2-x-feature-preview/57775

# navbar =  dbc.Navbar(
#              [
#                 dbc.NavItem(
#                     [
#                         dbc.NavLink(
#                             page["name"],
#                             href=(page["relative_path"]),
#                             className="nav-link",
#                         )
#                         for page in dash.page_registry.values()
#                     ],
#                     className="nav-item",
#                 ),
#             ],
#             className="navbar navbar-dark bg-primary",
#         )

# layout = html.Div(
#      [
#         navbar,
#         dash.page_container,
#      ]
#  )
 


if __name__ == "__main__":
    app.run_server(debug=True, port=8666)



#server = app.server
#app = Dash(__name__, use_pages=True)


# Bootstrap style layout in a container
# layout = dbc.Container(
#      [
#          dbc.Navbar(
#              [
#                  dbc.NavItem(
#                      [
#                          dbc.NavLink(
#                              page["name"],
#                              href=(page["relative_path"]),
#                              className="nav-link",
#                          )
#                          for page in dash.page_registry.values()
#                      ],
#                      className="nav-item",
#                  ),
#              ],
#              className="navbar navbar-dark bg-primary",
#          ),
#          dash.page_container,
#      ]
#  )



# Bootstrap style layout in a container
# layout = dbc.Container(
# dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="NavbarSimple",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )
# )

"""
FIGURE OUT HOW TO LINK NAVI CODE TO MULTI PAGES
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

if __name__ == '__main__':
	app.run_server(debug=True, port=8067)

"""
