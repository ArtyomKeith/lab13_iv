import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import folium_static
import requests
from folium import plugins

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Преобразуем GeoJSON в GeoDataFrame
gdf = gpd.read_file(url)

# Создаем карту на основе Microsoft Azure
m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True)

# Добавляем GeoJSON на карту
folium.GeoJson(geojson_data).add_to(m)

# Добавляем панель поиска по зданиям
search = plugins.Search(
    layer=folium.GeoJson(geojson_data),
    placeholder="Поиск зданий...",
    collapsed=True
)
search.add_to(m)

# Добавляем возможность выбора зданий через фильтрацию
st.title('Кампус Университета')
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

if building != 'Все':
    # Фильтруем по выбранному зданию
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": [feature for feature in geojson_data['features'] if feature['properties']['name'] == building]
    }
    folium.GeoJson(filtered_geojson).add_to(m)
else:
    folium.GeoJson(geojson_data).add_to(m)

# Отображаем карту
folium_static(m)

# Добавляем кнопки
st.markdown("### Дополнительные функции")
if st.button("Сбросить все фильтры"):
    folium.GeoJson(geojson_data).add_to(m)
    folium_static(m)

if st.button("Показать все здания"):
    folium.GeoJson(geojson_data).add_to(m)
    folium_static(m)
