import streamlit as st
import folium
import requests
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None):
    # Инициализация карты (убрали темную тему)
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True)

    # Добавляем кластер маркеров для улучшения взаимодействия с картой
    marker_cluster = MarkerCluster().add_to(m)

    # Добавление GeoJSON данных на карту (территория кампуса)
    folium.GeoJson(geojson_data, name="Campus Area", style_function=lambda x: {'fillColor': '#ff7800', 'color': 'black', 'weight': 1, 'fillOpacity': 0.4}).add_to(m)

    # Добавляем здания на карту
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':  # Добавляем только точки (здания)
            coords = feature['geometry']['coordinates']
            lat, lon = coords[1], coords[0]
            building_name = feature['properties']['name']
            building_description = feature['properties'].get('description', 'Описание отсутствует')
            
            # Выбираем иконку маркера в зависимости от типа здания
            building_type = feature['properties'].get('type', 'default')
            if building_type == 'administrative':
                icon = folium.Icon(color='blue', icon='info-sign')
            else:
                icon = folium.Icon(color='green', icon='cloud')

            # Создаем маркер с всплывающим окном, отображающим название и описание здания
            marker = folium.Marker([lat, lon], popup=f"<b>{building_name}</b><br>{building_description}", icon=icon)
            marker.add_to(marker_cluster)  # Добавляем маркер в кластер

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
    <h1 style="text-align: center;">Кампус Казахский агротехнический исследовательский университет имени С. Сейфуллина</h1>
""", unsafe_allow_html=True)

# Выпадающий список для выбора здания
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Если выбрано здание, создаем карту с приближением
if building != 'Все':
    create_map(building)
else:
    # Если не выбрано конкретное здание, показываем все
    create_map()
