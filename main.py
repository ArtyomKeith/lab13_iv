import streamlit as st
import folium
import requests
from streamlit_folium import folium_static

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None):
    # Инициализация карты
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True)

    # Добавляем территорию кампуса (многоугольник)
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Polygon':  # Добавляем территорию кампуса
            folium.GeoJson(feature, name="Campus Area").add_to(m)

    # Добавление только точечных объектов (здания) из GeoJSON
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':  # Только точки
            coords = feature['geometry']['coordinates']
            lat, lon = coords[1], coords[0]
            folium.Marker([lat, lon], popup=feature['properties']['name']).add_to(m)

    # Если выбрано здание, находим его и приближаем
    if selected_building:
        for feature in geojson_data['features']:
            if feature['properties']['name'] == selected_building:
                coords = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Point':
                    lat, lon = coords[1], coords[0]
                    m.fit_bounds([[lat - 0.002, lon - 0.002], [lat + 0.002, lon + 0.002]])

    # Отображаем карту
    folium_static(m)

# Заголовок без значка скрепки с помощью CSS
st.markdown("""
    <style>
        .streamlit-expanderHeader {
            display: none;
        }
    </style>
    <h1 style="text-align: center;">Кампус Университета</h1>
""", unsafe_allow_html=True)

# Выпадающий список для выбора здания
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Если выбрано здание, создаем карту с приближением
if building != 'Все':
    create_map(building)
else:
    # Если не выбрано конкретное здание, показываем все
    create_map()
