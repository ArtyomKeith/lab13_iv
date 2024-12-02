import streamlit as st
import folium
import requests
from streamlit_folium import folium_static

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None, map_type="Stamen Terrain"):
    # Инициализация карты с выбором типа карты
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True, tiles=map_type)

    # Добавление GeoJSON данных на карту
    folium.GeoJson(geojson_data, name="Campus").add_to(m)

    # Если выбрано здание, находим его и приближаем
    if selected_building:
        for feature in geojson_data['features']:
            if feature['properties']['name'] == selected_building:
                # Извлекаем координаты здания
                coords = feature['geometry']['coordinates']
                
                # Если это точка (Point), то координаты будут в формате [lon, lat]
                if feature['geometry']['type'] == 'Point':
                    lat, lon = coords[1], coords[0]
                    # Добавляем маркер на здание
                    folium.Marker([lat, lon], popup=feature['properties']['name']).add_to(m)

                    # Приближаем к этому зданию, чтобы здание было в центре экрана
                    m.fit_bounds([[lat - 0.002, lon - 0.002], [lat + 0.002, lon + 0.002]])

                # Если это полигоны (например, здания с несколькими углами), то извлекаем координаты для этих полигонов
                elif feature['geometry']['type'] == 'Polygon':
                    # Получаем минимальные и максимальные координаты полигона для fit_bounds
                    latitudes = [coord[1] for coord in coords[0]]
                    longitudes = [coord[0] for coord in coords[0]]
                    bounds = [[min(latitudes), min(longitudes)], [max(latitudes), max(longitudes)]]
                    m.fit_bounds(bounds)

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

# Кнопки для выбора действия
col1, col2 = st.columns(2)

with col1:
    if st.button('Показать все здания'):
        create_map()

with col2:
    building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])
    if building != 'Все' and st.button('Показать здание'):
        create_map(building)

# Переключение типов карт
map_type = st.selectbox(
    'Выберите тип карты',
    ['Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'OpenStreetMap']
)

# Информация о выбранном здании
if building != 'Все':
    selected_building_info = next(feature for feature in geojson_data['features'] if feature['properties']['name'] == building)
    st.markdown(f"### Информация о здании: {selected_building_info['properties']['name']}")
    st.write(f"Тип здания: {selected_building_info['properties']['type']}")
    st.write(f"Описание: {selected_building_info['properties']['description']}")
else:
    st.write("Выберите здание для отображения его информации.")
