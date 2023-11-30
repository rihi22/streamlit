import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import folium
import matplotlib.pyplot as plt
import pydeck as pdk
import contextily as ctx
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_vega_lite import vega_lite_component
from vega_datasets import data


# Charger le fichier Shapefile des communes du Maroc
shapefile_path = "maroc_region.shp"
maroc = gpd.read_file(shapefile_path)



# Créer une carte Folium centrée sur le Maroc
m = folium.Map(location=[maroc.geometry.centroid.y.mean(), maroc.geometry.centroid.x.mean()], zoom_start=6)

# Ajouter les communes au fond de carte
folium.GeoJson(maroc).add_to(m)


# Définir les limites du Maroc à partir du shapefile
maroc_polygon = maroc.unary_union

# Générer des points aléatoires au Maroc
num_points = 300
points_inside_maroc = []
while len(points_inside_maroc) < num_points:
    lon = np.random.uniform(maroc_polygon.bounds[0], maroc_polygon.bounds[2])
    lat = np.random.uniform(maroc_polygon.bounds[1], maroc_polygon.bounds[3])
    point = Point(lon, lat)
    if point.within(maroc_polygon):
        points_inside_maroc.append(point)

# Créer une géodataframe avec les colonnes spécifiées dans le schéma
df = pd.DataFrame({
    'Geometry': points_inside_maroc,
    'Propriete1': np.random.choice(['A', 'B', 'C'], size=num_points),
    'Propriete2': np.random.uniform(low=0, high=100, size=num_points),
    'Propriete3': np.random.uniform(low=0, high=100, size=num_points),
    'Propriete4': pd.date_range('2022-01-01', periods=num_points),
})
for i in range(7):
        df[f'Attribut1Jour-{i}'] = np.random.uniform(low=0, high=100, size=num_points)
        df[f'Attribut2Jour-{i}'] = np.random.uniform(low=0, high=20, size=num_points)
        df[f'Attribut3Jour-{i}'] = np.random.uniform(low=0, high=50, size=num_points)

df = pd.DataFrame(df)
gdf = gpd.GeoDataFrame(df, geometry='Geometry')
# Convertir le DataFrame en GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='Geometry')

# Filtrer les points pour qu'ils soient à l'intérieur des limites du Maroc
gdf = gdf[gdf.geometry.within(maroc.unary_union)]

# Sauvegarder en format Geoparquet
gdf.to_parquet('dataset_geoparquet_maroc.geoparquet', index=False)
# Titre de l'application
st.title('Dashboard GeoAnalytique')

# Extraire les coordonnées de latitude et de longitude de la colonne Geometry
gdf['Latitude'] = gdf['Geometry'].apply(lambda point: point.y)
gdf['Longitude'] = gdf['Geometry'].apply(lambda point: point.x)

# Afficher une carte avec les points
st.map(gdf, latitude='Latitude', longitude='Longitude')

# Afficher le tableau de données
st.write(gdf)

