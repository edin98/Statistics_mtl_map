from dash import dcc, html, Dash, dash_table, callback, Input, Output
import pandas as pd
import plotly.express as px
import geopandas as gpd
import json
import plotly
from plotly.graph_objs import layout

app = Dash(__name__)

my_style = {
    'backgroundColor': '#090909',
    'fontFamily': 'Times New Roman',
    'color': '#a2a2a2',
    'text-align': 'center',
    'padding': -5,
    'marginBottom': -25,
    'marginLeft': -8,
    'marginRight': -8,
    'marginTop': -23}
# Importing the geometric data
with open("./data/montreal_dissemination_areas2.geojson",
          encoding='utf-8') as geofile:
    j_file = json.load(geofile)

# Importing the population data
population_data = pd.read_csv('./data/mtl_pop.csv')
mtl_household_type = pd.read_csv('./data/mtl_household_type.csv')
mtl_income = pd.read_csv('./data/mtl_income.csv')
pd.options.display.float_format = '{:,.2f}'.format

all_options = {
    'population': population_data,
    'households': mtl_household_type,
    'income': mtl_income
}

# APP LAYOUT
app.layout = html.Div(
    style=my_style,
    children=[
        html.H1("Montreal Statistics' Map by Area", className='text-primary text-center', style={"color": "lightgrey", 'fontFamily': 'Times New Roman'}),
        html.P('Created by Edinson J. Arita'),
        html.Div([
            dcc.RadioItems(
                list(all_options.keys()),
                'population',
                inline=True,
                id='dataset_choice'
            )]),
        html.Div([
            dcc.Dropdown(
                id='columns',
                options=[],
                style={
                    'backgroundColor': 'lightgrey',
                    'text-align': 'center',
                    'fontFamily': 'Times New Roman',
                    'padding': 0,
                    'marginBottom': 0,
                    'color': 'black'})],  # this is the color of letters inside the dropdown
            style={
                'backgroundColor': 'black',
                'text-align': 'center',
                'padding': 0,
                'marginBottom': 0,
                'color': 'black'
            },
            className='row'),

        html.Div(
            dcc.Graph(id='graph', figure={})
        )
    ])


@callback(
    Output(component_id='columns', component_property='options'),
    Input(component_id='dataset_choice', component_property='value'))
def set_dataset_options(dataset):
    return [{'label': i, 'value': i} for i in all_options[dataset]]


@callback(
    Output('columns', 'value'),
    Input('columns', 'options'))
def set_dataset_value(available_options):
    return available_options[1]['value']


@app.callback(
    Output(component_id='graph', component_property='figure'),

    [Input(component_id='dataset_choice', component_property='value'),
     Input(component_id='columns', component_property='value')]
)
def update_map(dataset, chosen_val):
    print(f'user chose {dataset} and the column {chosen_val}')
    df0 = all_options[dataset]
    df = df0[['DAUID', chosen_val]]
    fig = px.choropleth_mapbox(
        df,
        geojson=j_file,
        locations='DAUID',
        featureidkey='properties.DAUID',
        color=chosen_val,
        opacity=0.4,
        mapbox_style='carto-darkmatter',
        zoom=9,
        center={'lat': 45.52, 'lon': -73.70},
        color_continuous_scale='turbo',
        height=608).update_layout(
        paper_bgcolor='#090909',
        font_color='white',
        margin=dict(l=0, r=0, b=0, t=0),
        margin_pad=0,

        margin_autoexpand=True, ).update_coloraxes(
        colorbar_borderwidth=0,
        colorbar_title='',
        colorbar_bordercolor='#171817',
        colorbar_len=1,
        colorbar_orientation='h',
        colorbar_outlinewidth=1,
        colorbar_thickness=15,
        colorbar_outlinecolor='white',
        colorbar_ticklabelposition='outside right',
        colorbar_ticks='inside',
        colorbar_tickfont_color='white',
        colorbar_tickfont_family='Times New Roman',
        colorbar_title_side='top',
        colorbar_title_font_family='Times New Roman')

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
