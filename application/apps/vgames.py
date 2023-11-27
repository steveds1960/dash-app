from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

dfv = pd.read_csv(DATA_PATH.joinpath("vgsales.csv"))  # GregorySmith Kaggle
sales_list = ["North American Sales", "EU Sales", "Japan Sales", "Other Sales",	"World Sales"]





layout = html.Div([
    html.H1('Video Games Sales', style={"textAlign": "center"}),

    dbc.Container([
        dbc.Label('Click a cell in the table:'),
        dash_table.DataTable(id='table', columns=[{'name': i, 'id': i} for i in sorted(dfv.head(0).columns)]),
        dbc.Alert(id='tbl_out'),
        ]),

    html.Div([
        html.Div([
            html.Pre(children="Genre", style={"fontSize":"150%"}),
            dcc.Dropdown(
                id='genre-dropdown', value='DEBIT', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x} for x in sorted(dfv.Genre.unique())]
            )], className='four columns'),

        html.Div([
            html.Pre(children="Sales to sort", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='sales-dropdown', value='EU Sales', clearable=False,
                persistence=True, persistence_type='memory',
                options=[{'label': x, 'value': x} for x in sales_list]
            )], className='four columns')
    ], className='row'),

    dcc.Graph(id='my-bar', figure={})
])


@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)

def display_value(genre_chosen, sales_chosen):
    dfv_fltrd = dfv[dfv['Genre'] == genre_chosen] # 1st data filtering
    dfv_fltrd = dfv_fltrd.nlargest(10, sales_chosen) # 2nde data filtering
    fig = px.bar(dfv_fltrd, x='Video Game', y=sales_chosen, color='Platform')
    fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig

@app.callback(
    Output(component_id='table', component_property='data'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)
def update_table(genre_chosen, sales_chosen):
    dfv_fltrd = dfv[dfv['Genre'] == genre_chosen] # 1st data filtering
    dfv_fltrd = dfv_fltrd.nlargest(10, sales_chosen) # 2nde data filtering
    return dfv_fltrd.head(5).to_dict('records')