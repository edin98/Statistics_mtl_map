from dash import dcc, html, Dash, dash_table, callback, Input, Output
import pandas as pd
import plotly.express as px
import geopandas as gpd
import dash_bootstrap_components as dbc
import json

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

#Importing the geometric data
with open("./data/montreal_dissemination_areas2.geojson",
          encoding='utf-8') as geofile:
    j_file = json.load(geofile)

#Importing the population data
population_data = pd.read_csv('./data/mtl_pop.csv')
pd.options.display.float_format = '{:,.2f}'.format

#Building the map and link with data
fig = px.choropleth_mapbox(
    population_data,
    geojson=j_file,
    locations='DAUID',
    featureidkey='properties.DAUID',
    color='Median age of the population',
    opacity=0.4,
    mapbox_style='open-street-map',
    zoom=9,
    center={'lat': 45.52, 'lon': -73.70},
    height=800)
fig.update_geos(fitbounds='locations', visible=False)


# APP LAYOUT
app.layout = html.Div([

    html.H1('Dash Project!', className='text-primary text-center'),
    html.Div('Interactive Graph', className="text-primary text-center fs-3"),

    html.Div(
        dcc.Graph(figure=fig, responsive=True))
    ])



if __name__ == "__main__":
    app.run_server()
