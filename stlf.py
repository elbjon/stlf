import streamlit as st
import folium
from streamlit_folium import folium_static

# Create a Folium map
m = folium.Map(location=[51.1657, 10.4515], zoom_start=5)

# Add ImageOverlays to the map
img_overlay_1 = folium.raster_layers.ImageOverlay(
    name="Overlay 1",
    image="img/224m1765-279-00488_it1_thresholded.jpg",
    bounds=[[50, 10], [52, 12]],
    opacity=0.6,
    interactive=True,
)
img_overlay_1.add_to(m)

img_overlay_2 = folium.raster_layers.ImageOverlay(
    name="Overlay 2",
    image="img/224m1765-279-00488_it1_thresholded.jpg",
    bounds=[[53, 11], [55, 13]],
    opacity=0.6,
    interactive=True,
)
img_overlay_2.add_to(m)

# Add placeholder GeoJSON layers with custom colors for the LayerControl
placeholder_geojson_1 = folium.GeoJson(
    {"type": "Point", "coordinates": [0, 0]},
    name="Overlay 1",
    style_function=lambda x: {"fillColor": "blue", "color": "blue"},
)
placeholder_geojson_1.add_to(m)

placeholder_geojson_2 = folium.GeoJson(
    {"type": "Point", "coordinates": [0, 0]},
    name="Overlay 2",
    style_function=lambda x: {"fillColor": "green", "color": "green"},
)
placeholder_geojson_2.add_to(m)

# Display the map in Streamlit
folium_static(m)
#test

#############################################

# Create a Folium map
m = folium.Map(location=[51.1657, 10.4515], zoom_start=5)

# Add some layers to the map
folium.TileLayer("OpenStreetMap").add_to(m)
folium.TileLayer("Stamen Terrain").add_to(m)
folium.TileLayer("Stamen Toner").add_to(m)

# Create a LayerControl with custom colors
layer_control_html = """
    <div style="
        position: fixed; 
        top: 10px; 
        left: 10px; 
        width: 120px; 
        height: 110px; 
        border: 2px solid grey; 
        z-index: 1002;
        background-color: white;
        opacity: 0.8;
    ">
        <p style="margin: 5px;">
            <span style="color: #1f77b4;">&#9679;</span> OpenStreetMap
        </p>
        <p style="margin: 5px;">
            <span style="color: #ff7f0e;">&#9679;</span> Terrain
        </p>
        <p style="margin: 5px;">
            <span style="color: #2ca02c;">&#9679;</span> Toner
        </p>
    </div>
"""

# Add the custom LayerControl to the map
folium.Marker([0, 0], icon=folium.DivIcon(html=layer_control_html)).add_to(m)

# Display the map in Streamlit
folium_static(m)