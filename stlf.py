import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
st.write('Some Random Square Grids')




# Create a map using the Map() function and the coordinates for Boulder, CO
m = folium.Map(location=[52.8, 10.8], zoom_start=6, tiles="cartodb positron")

#tile = folium.TileLayer(
#        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#        attr = 'Esri',
#        name = 'Esri Satellite',
#        overlay = False,
#        control = True
#       ).add_to(m)


#add polygons




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

folium.Marker(
    [52.8, 10.8], popup="HELLO", tooltip="HELLOHELLO"
).add_to(m)

folium_static(m)
