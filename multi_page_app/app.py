# import necessary libraries
import dash
from dash import Dash
import dash_bootstrap_components as dbc


#Create Dash app instance, as argument pass Bootstrap flatly template to achieve consistent sytling in each page 
app = Dash(
    __name__,
    use_pages=True,
    pages_folder="apps",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ]
)


# Below code for Navbar is adapted from Chris Parmer's -Co-founder of Plotly, Author of Dash- feature preview of '/pages'
# Available at community.plotly: https://community.plotly.com/t/introducing-dash-pages-a-dash-2-x-feature-preview/57775

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
        dash.page_container
      ]
)


# run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True, port=8667)



