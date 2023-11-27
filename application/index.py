from doctest import debug
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# connect to the main app.py file
from app import app
from app import server

# connect to app pages

from apps import vgames, global_sales

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Video Games | ', href='/apps/vgames'),
        dcc.Link('Other products', href='/apps/global_sales'),
    ], className='row'),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/vgames': return vgames.layout
    if pathname == '/apps/global_sales': return global_sales.layout
    else: return '404 Page Error! Please choose a link'

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')