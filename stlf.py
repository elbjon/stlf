import os
import streamlit as st
import folium
from streamlit_folium import folium_static

# Get the path to the directory containing the images
img_folder = 'img'  # Replace with your actual folder name
img_path = os.path.join(os.path.dirname(__file__), img_folder)

# Erstelle eine Karte
m = folium.Map(location=[51.5, 10], zoom_start=7)

# Erstelle eine FeatureGroup für die Overlays
overlay_group = folium.FeatureGroup(name='Overlays')

# Füge die Overlays zur FeatureGroup hinzu
image_files = sorted([f for f in os.listdir(img_path) if f.endswith('.jpg')])
for i, img_file in enumerate(image_files, start=1):
    img_path = os.path.join(img_folder, img_file)
    overlay = folium.raster_layers.ImageOverlay(
        name=f'Overlay_{i}',
        image=img_path,
        bounds=[[51.85, 9.6], [53.3, 11.70]],
        opacity=0.6,
        interactive=True,
        cross_origin=False,
        zindex=i
    )
    overlay.add_to(overlay_group)

    # Group images in sets of four
    if i % 4 == 0:
        # Füge die FeatureGroup zur Karte hinzu
        overlay_group.add_to(m)
        # Erstelle eine neue FeatureGroup für die nächsten Overlays
        overlay_group = folium.FeatureGroup(name=f'Overlays{i}')

# Füge eine weitere Layer Control für die FeatureGroup hinzu
folium.LayerControl(collapsed=False).add_to(m)

# Zeige die Karte mit streamlit_folium
folium_static(m)
