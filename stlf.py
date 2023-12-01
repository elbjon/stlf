from folium import Map, TileLayer, LayerControl
import folium
from streamlit_folium import st_folium

# Create a Folium map
m = Map(location=[51.5, -0.1], zoom_start=10)

# Add tile layers
TileLayer("OpenStreetMap").add_to(m)
TileLayer("cartodb positron").add_to(m)

# Create a Layer Control
layer_control = LayerControl().add_to(m)

# Inject custom CSS styles
custom_css = """
<style>
.leaflet-control-layers-list {
    color: red;  /* Change the text color to red */
    /* Add more custom styles as needed */
}
</style>
"""

m.get_root().html.add_child(folium.Element(custom_css))

# Display the map
m

# Create a Folium map
m = Map(location=[51.5, -0.1], zoom_start=10)

# Add tile layers
TileLayer("OpenStreetMap").add_to(m)
TileLayer("cartodb positron").add_to(m)

# Create a Layer Control
layer_control = LayerControl().add_to(m)

# Inject custom CSS styles
custom_css = """
<style>
.leaflet-control-layers-list {
    color: red;  /* Change the text color to red */
    /* Add more custom styles as needed */
}
</style>
"""

m.get_root().html.add_child(folium.Element(custom_css))

# Display the map
st_folium(m)