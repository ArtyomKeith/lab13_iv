import streamlit as st
import folium
import requests
from streamlit_folium import folium_static

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None, zoom_level=16):
    # Инициализация карты
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=zoom_level, control_scale=True)

    # Добавление GeoJSON данных на карту
    folium.GeoJson(geojson_data, name="Campus").add_to(m)

    # Если выбрано здание, находим его и добавляем маркер с информацией
    if selected_building:
        for feature in geojson_data['features']:
            if feature['properties']['name'] == selected_building:
                # Извлекаем координаты здания
                coords = feature['geometry']['coordinates']
                
                # Если это точка (Point), то координаты будут в формате [lon, lat]
                if feature['geometry']['type'] == 'Point':
                    lat, lon = coords[1], coords[0]
                    # Добавляем маркер с дополнительной информацией
                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(f"<b>{feature['properties']['name']}</b><br>{feature['properties']['description']}", max_width=300)
                    ).add_to(m)

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

# Выпадающий список для выбора здания
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Слайдер для выбора уровня увеличения карты
zoom_level = st.slider('Выберите уровень увеличения карты', min_value=10, max_value=20, value=16)

# Если выбрано здание, создаем карту с приближением
if building != 'Все':
    create_map(building, zoom_level)
else:
    # Если не выбрано конкретное здание, показываем все
    create_map(zoom_level=zoom_level)
