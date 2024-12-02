import streamlit as st
import folium
import requests
from streamlit_folium import folium_static
from folium.plugins import Search, MarkerCluster
from geopy.distance import geodesic

# Загружаем GeoJSON с GitHub
url = "https://raw.githubusercontent.com/ArtyomKeith/lab13_iv/main/campus.geojson"
geojson_data = requests.get(url).json()

# Функция для отображения карты с приближением на выбранное здание
def create_map(selected_building=None, map_type='OpenStreetMap', building_a=None, building_b=None):
    # Инициализация карты с возможностью переключения между картами
    m = folium.Map(location=[51.1879, 71.4085], zoom_start=16, control_scale=True)

    # Добавление карт: OpenStreetMap, Esri, Google Maps
    folium.TileLayer(map_type).add_to(m)

    # Инициализация кластера маркеров
    marker_cluster = MarkerCluster().add_to(m)

    # Добавление GeoJSON данных на карту
    folium.GeoJson(geojson_data, name="Campus").add_to(m)

    # Добавление маркеров для каждого здания
    for feature in geojson_data['features']:
        building_name = feature['properties']['name']
        coords = feature['geometry']['coordinates']
        
        # Если это точка (Point), то координаты будут в формате [lon, lat]
        if feature['geometry']['type'] == 'Point':
            lat, lon = coords[1], coords[0]
            
            # Добавляем маркер с попапом
            popup_content = f"<strong>{building_name}</strong><br>Подробнее о здании..."
            folium.Marker([lat, lon], popup=popup_content).add_to(marker_cluster)
            
            # Приближаем к этому зданию, если оно выбрано
            if selected_building == building_name:
                m.fit_bounds([[lat - 0.002, lon - 0.002], [lat + 0.002, lon + 0.002]])

            # Если указаны два здания, строим маршрут между ними
            if building_a and building_b:
                if building_a == building_name or building_b == building_name:
                    if building_a == building_name:
                        lat_a, lon_a = lat, lon
                    if building_b == building_name:
                        lat_b, lon_b = lat, lon
                        
    # Строим маршрут между двумя зданиями
    if building_a and building_b and lat_a and lat_b:
        folium.PolyLine([(lat_a, lon_a), (lat_b, lon_b)], color='blue', weight=2.5, opacity=1).add_to(m)

        # Вычисляем расстояние между двумя зданиями
        distance = geodesic((lat_a, lon_a), (lat_b, lon_b)).km
        folium.Marker([(lat_a + lat_b) / 2, (lon_a + lon_b) / 2],
                      popup=f"Расстояние: {distance:.2f} км").add_to(m)

    # Поиск по названию зданий
    search = Search(layer=folium.GeoJson(geojson_data)).add_to(m)

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

# Выбор типа карты
map_type = st.selectbox("Выберите тип карты", ['OpenStreetMap', 'Esri', 'Stamen Terrain'])

# Выпадающий список для выбора здания
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Выпадающие списки для выбора зданий для маршрута
building_a = st.selectbox('Выберите первое здание для маршрута', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])
building_b = st.selectbox('Выберите второе здание для маршрута', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Если выбрано здание, создаем карту с приближением
if building != 'Все':
    create_map(selected_building=building, map_type=map_type, building_a=building_a if building_a != 'Все' else None, building_b=building_b if building_b != 'Все' else None)
else:
    # Если не выбрано конкретное здание, показываем все
    create_map(map_type=map_type, building_a=building_a if building_a != 'Все' else None, building_b=building_b if building_b != 'Все' else None)
