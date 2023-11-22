import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static

st.write('Some Random Square Grids')

df=pd.read_csv('mappingtestPolg_s.csv')



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



    
# Iterate through the DataFrame rows
for index, row in df.iterrows():
#    # Convert the string representation of the list to an actual list of coordinates
#    polygon_coords = ast.literal_eval(row['Polygon'])
#    
    folium.Polygon(
        locations=row['Polygon'], #polygon_coords,
        color='darkgreen',
        weight=1,
        fill_color='green',
        fill=True,
        popup=row['Title_short'],  # Use the Title_short column as popup content
        tooltip=row['Title_short'],
    ).add_to(m)


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
