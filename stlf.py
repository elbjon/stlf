import streamlit as st
import folium
import streamlit_folium




st.write('hello world')

# Create a map using the Map() function and the coordinates for Boulder, CO
m = folium.Map(location=[52.8, 10.8], tiles="cartodb positron")

# Display the map
m

















# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="HELLO", tooltip="HELLOHELLO"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

st_data

folium_static(m)
