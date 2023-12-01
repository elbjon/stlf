import streamlit as st
import pandas as pd
import folium
from ast import literal_eval
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder
from PIL import Image
import json
import os

st.set_page_config(layout="wide")




# Image file path
image_path = "images/example_image.png"

# Load and display the image
image = Image.open('heatmap_Screenshot.png')
st.image(image, caption="Density of Photographic Reconnaissance Flights", use_column_width=False)





p = folium.Map(location=[30, 30], tiles=None, zoom_start=3)
folium.TileLayer("OpenStreetMap", name= 'OpenStreetMap').add_to(p)
folium.TileLayer("cartodb positron",show=False).add_to(p)
folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Satellite Image',
            show=False,
            overlay = False,
            control = True
           ).add_to(p)

folium.TileLayer(
    tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    name = 'Topographic Map',
    attr='opentopomap.org',
    show=False,
    ).add_to(p)

# Assuming 'img' folder is in the current working directory
img_folder = 'img'

# Iterate through each file in the 'img' folder
for count, file_name in enumerate(os.listdir(img_folder)):
    # Construct the file path
    img_path = os.path.join(img_folder, file_name)

    # Check if the file is an image (you may want to refine this check based on your specific image types)
    if os.path.isfile(img_path) and img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        
        # Create ImageOverlay with a unique name based on counting variable
        img_overlay = folium.raster_layers.ImageOverlay(
            name=f"Overlay_{count + 1}",
            image=img_path,
            bounds=[[51.85, 9.6], [53.3, 11.70]],  # Adjust the bounds accordingly
            opacity=0.6,
            show=False,
            interactive=False,
            cross_origin=False,
            control=True,
            zindex=count + 1,
        )

        # Add ImageOverlay to the map 'p'
        img_overlay.add_to(p)






folium.Marker(
    [52, 10], popup="52,10", tooltip="HELLOHELLO"
).add_to(p)
folium.Marker(
    [53, 10], popup="53, 10", tooltip="HELLOHELLO"
).add_to(p)
folium.Marker(
    [53, 11], popup="53, 11", tooltip="HELLOHELLO"
).add_to(p)
folium.Marker(
    [52, 11], popup="52, 11", tooltip="HELLOHELLO"
).add_to(p)

# add search field
Geocoder().add_to(p)

folium.LayerControl().add_to(p)


map = st_folium(p, height=800, width=1400)
st.write(map)
















    #For Polygon description etc look into the file from raspberry pi
    #folium.Polygon(
    #    locations=locations,
    #    color="blue",
    #    weight=1,
    #    fill_color="blue",
    #    fill_opacity=0.5,
    #    fill=True,
    #    popup="First Poly",
    #    tooltip="Click me!",
    #).add_to(m)




    #lat_interval = 10
    #lon_interval = 10

    #for lat in range(-90, 91, lat_interval):
    #     folium.PolyLine([[lat, -180],[lat, 180]], weight=2).add_to(m)

    #for lon in range(-180, 181, lon_interval):
    #    folium.PolyLine([[-90, lon],[90, lon]], weight=2).add_to(m)


