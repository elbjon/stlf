import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static

# Create a map using the Map() function and the coordinates for Boulder, CO
m = folium.Map(location=[52.8, 10.8], tiles="cartodb positron", zoom_start=5)

#add polygons
locations = [
[[49, 10], [50, 10], [50, 11], [49, 11]],
[[52, 4], [53, 4], [53, 5], [52, 5]],
[[52, 10], [53, 10], [53, 11], [52, 11]],
[[52, 11], [53, 11], [53, 12], [52, 12]],
[[52, 12], [53, 12], [53, 13], [52, 13]],
[[52, 13], [53, 13], [53, 14], [52, 14]],
[[54, 13], [55, 13], [55, 14], [54, 14]],
[[55, 4], [56, 4], [56, 5], [55, 5]]
]

#For Polygon description etc look into the file from raspberry pi
folium.Polygon(
    locations=locations,
    color="blue",
    weight=1,
    fill_color="blue",
    fill_opacity=0.5,
    fill=True,
    popup="First Poly",
    tooltip="Click me!",
).add_to(m)

folium.Marker(
    [52.8, 10.8], popup="HELLO", tooltip="HELLOHELLO"
).add_to(m)

folium_static(m)
