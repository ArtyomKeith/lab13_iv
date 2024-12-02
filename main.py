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

                    # Приближаем к этому зданию
                    m.fit_bounds([[lat - 0.002, lon - 0.002], [lat + 0.002, lon + 0.002]])

    # Отображаем карту
    folium_static(m)

# Заголовок
st.title('Кампус Университета')

# Выпадающий список для выбора здания
building = st.selectbox('Выберите здание', ['Все'] + [feature['properties']['name'] for feature in geojson_data['features']])

# Если выбрано здание, создаем карту с приближением
if building != 'Все':
    create_map(building)
else:
    # Если не выбрано конкретное здание, показываем все
    create_map()

# Дополнительные кнопки
st.markdown("### Дополнительные функции")
if st.button("Сбросить все фильтры"):
    create_map()
