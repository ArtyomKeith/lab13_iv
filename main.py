import folium
import pandas as pd
import geopandas as gpd
from shapely import wkt
import webbrowser

data = pd.read_csv("Универ.csv")

if 'geometry' not in data.columns:
    data['geometry'] = data['WKT'].apply(wkt.loads)

gdf = gpd.GeoDataFrame(data, geometry='geometry')

geometry = gdf.iloc[0]['geometry']
center = geometry.centroid

campus_map = folium.Map(location=[center.y, center.x], zoom_start=17)

folium.GeoJson(
    geometry,
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0.3
    }
).add_to(campus_map)

campus_map.fit_bounds(geometry.bounds)

campus_map.save("campus_map.html")

webbrowser.open("campus_map.html")
