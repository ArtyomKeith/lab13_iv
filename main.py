import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# URL вашего GeoJSON-файла на GitHub
geojson_url = "https://github.com/ArtyomKeith/lab13_iv/blob/main/campus.geojson"

# Загрузка GeoJSON
@st.cache_data
def load_geojson(url):
    gdf = gpd.read_file(url)
    return gdf

# Загрузка данных
gdf = load_geojson(geojson_url)

# Центр карты (вычисляем автоматически)
center_lat = gdf.geometry.centroid.y.mean()
center_lon = gdf.geometry.centroid.x.mean()

# Создание карты с Folium
st.title("Интерактивная карта кампуса")
campus_map = folium.Map(location=[center_lat, center_lon], zoom_start=17, tiles="Stamen Terrain")

# Добавление данных на карту
for _, row in gdf.iterrows():
    coords = row.geometry.exterior.coords if row.geometry.type == "Polygon" else row.geometry.coords
    popup_text = f"<b>{row['название']}</b><br>{row['описание']}"
    if row.geometry.type == "Polygon":
        folium.Polygon(
            locations=[(lat, lon) for lon, lat in coords],
            color="blue",
            fill=True,
            fill_opacity=0.4,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(campus_map)

# Отображение карты в Streamlit
st_data = st_folium(campus_map, width=700, height=500)
