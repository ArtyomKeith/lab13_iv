import streamlit as st
import folium
import requests
from streamlit_folium import folium_static

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None, map_type="light", building_a=None, building_b=None):
    # Инициализация карты
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True)

    # Добавление GeoJSON данных на карту
    folium.GeoJson(geojson_data, name="Campus").add_to(m)

    # Проверяем, если выбраны два здания, извлекаем их координаты
    if building_a and building_b:
        lat_a, lon_a, lat_b, lon_b = None, None, None, None
        
        for feature in geojson_data['features']:
            # Проверяем, совпадает ли имя с building_a и building_b
            if feature['properties']['name'] == building_a:
                coords_a = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Point':
                    lat_a, lon_a = coords_a[1], coords_a[0]

            if feature['properties']['name'] == building_b:
                coords_b = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Point':
                    lat_b, lon_b = coords_b[1], coords_b[0]

        if lat_a and lat_b:
            # Добавляем маркеры для зданий A и B
            folium.Marker([lat_a, lon_a], popup=building_a).add_to(m)
            folium.Marker([lat_b, lon_b], popup=building_b).add_to(m)
            
            # Приближаем карту, чтобы включить оба здания
            m.fit_bounds([[lat_a - 0.002, lon_a - 0.002], [lat_b + 0.002, lon_b + 0.002]])

    # Если выбрано одно здание, приближаем только его
    elif selected_building:
        for feature in geojson_data['features']:
            if feature['properties']['name'] == selected_building:
                coords = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Point':
                    lat, lon = coords[1], coords[0]
                    folium.Marker([lat, lon], popup=selected_building).add_to(m)
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
building_a = st.selectbox('Выберите первое здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])
building_b = st.selectbox('Выберите второе здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Если выбраны здания, создаем карту с приближением
if building_a != 'Все' and building_b != 'Все':
    create_map(building_a=building_a, building_b=building_b)
else:
    # Если не выбраны конкретные здания, показываем все
    selected_building = st.selectbox('Выберите здание для приближения', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])
    if selected_building != 'Все':
        create_map(selected_building=selected_building)
    else:
        create_map()
