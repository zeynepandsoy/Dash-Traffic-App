import dash
from dash import html
import dash_bootstrap_components as dbc

#define path to the home page
dash.register_page(__name__, path='/')

#Using direct image file path
image_path = 'assets/Google-Maps:I-94.png'

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1(children='Dashboard app of Minneapolis-St Paul, MN traffic volume for westbound I-94 between 2012 and 2018',
                        style={"color": "#00008B","text-align": "center"}),
                width=12)
            ]),

    dbc.Row([
        dbc.Col(html.Img(src=image_path,
                         style={'height':'100%', 'width':'60%'}))
                
            ], style={'textAlign': 'center'})
      
    ])

           