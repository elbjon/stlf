import streamlit as st
import pandas as pd
import folium
from ast import literal_eval
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder
import json
import os

st.set_page_config(layout="wide")



st.write('Choose your continent of interest by clicking')
#########################
# Function to embed GeoJSON data
def embed_geojson_from_github(folder, file_name):
    # Assuming the GeoJSON file is stored in the 'polygons' folder
    file_path = f"{folder}/{file_name}"
    with open(file_path, 'r') as file:
        geojson_data = json.load(file)
    return geojson_data

# GitHub repo folder and file
github_folder = "polygons"
geojson_file = "World_Continents.geojson"

# Fetch GeoJSON data
geojson_data = embed_geojson_from_github(github_folder, geojson_file)

# Create a Folium map
m = folium.Map(location=[30, 10], zoom_start=2)

# Check if GeoJSON data is available
if geojson_data:
    # Add GeoJSON layer to the map
    folium.GeoJson(geojson_data, name='geojson').add_to(m)

    # Display the map using Streamlit
    mabb = st_folium(m, height=1000, width=1400,returned_objects=["last_active_drawing"])

    
    if mabb and 'last_active_drawing' in mabb:
        continent = mabb['last_active_drawing']['properties']['CONTINENT']
        fid = mabb['last_active_drawing']['properties']['FID']
        st.write(continent, fid)
    else:
        st.warning("Please use the drawing tool to select a continent.")


    #if mabb is not None:
    #    st.write(mabb['last_active_drawing']['properties']['CONTINENT'],mabb['last_active_drawing']['properties']['FID'])

    #if map.get("last_clicked"):
    #    data = mabb["last_clicked"]["lat"], mabb["last_clicked"]["lng"]




else:
    st.warning("No GeoJSON data available.")




###########################






data = [52, 10]
choice = st.radio(
    "Set scale:",
    ["Overview Map", "Detail Map"],
    index=0,
)


st.write("You selected:", choice)



urla = r'https://www.archives.gov/findingaid/stat/discovery/373'
st.write(f'Density of Aerial Reconnaissance Flights as documented in NARA\'s',"[Record Group 373](%s)" % urla)

#st.write("Link to [RG 373](%s)" % urla)
#df=pd.read_csv('base_data.csv')
#df = pd.read_csv('base_data.csv',converters={"Polygon": lambda x: x.strip("[]").split(", ")})
df = pd.read_csv('base_data.csv',converters={'Polygon': literal_eval})
st.write('loading takes a minute or two')


if choice == 'Overview Map':

    # coord getter function
    def get_pos(lat, lng):
        return lat, lng


    # Create a map using the Map() function and the coordinates for Boulder, CO
    m = folium.Map(zoom_start=6, tiles="cartodb positron",height=900, width=1200,returned_objects=["last_object_clicked"])
    #bounds = folium.get_bounds(m)
    #print("Bounds:", bounds)
    



    #add polygons

    #path = r'https://catalog.archives.gov/id/'
        
    # Iterate through the DataFrame rows
    #for index, row in df.iterrows():
    #    # Convert the string representation of the list to an actual list of coordinates
    #    polygon_coords = row['Polygon']
    #    a, b = row['Title_short'], row['Overlay_sheet_ct']
    #    dest = row['naId'] 
    #    opac=int(row['Overlay_sheet_ct'])/100 #geht, weil keine 0 vorhanden in diesem Dataset
    #    folium.Polygon(
    #        locations=polygon_coords,
    #        color='green',
    #        weight=0.1,
    #        opacity=opac/2,
    #        fill_color='green',
    #        fill_opacity=opac,
    #        fill=True,
    #        popup=f"<a href={path}{dest} target='_blank'>To Map Overlays</a>", #row['Title_short'],  # Use the Title_short column as popup content
    #        #tooltip=f'{a}, {b} Overlay sheets' ,
    #    ).add_to(m)
    







    folium.Marker(
        [52.8, 10.8], popup="HELLO", tooltip="HELLOHELLO"#
    ).add_to(m)

    folium.Marker(
        [45, -124], popup="45,-124", tooltip="HELLOHELLO"
    ).add_to(m)
    folium.Marker(
        [46, -124], popup="46, -124", tooltip="HELLOHELLO"
    ).add_to(m)
    folium.Marker(
        [46, -123], popup="46, -123", tooltip="HELLOHELLO"
    ).add_to(m)
    folium.Marker(
        [45, -124], popup="45, -124", tooltip="HELLOHELLO")


    #add latitude/longitude popup
    m.add_child(folium.LatLngPopup())

    # add search field
    Geocoder().add_to(m)




    #folium_static(m)
    map = st_folium(m, height=900, width=1400)

    data = None
    if map.get("last_clicked"):
        dada = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(dada) # Writes to the app
        #print(data) # Writes to terminal
        choice = "Detail Map"
        

elif choice == "Detail Map":
    
    st.write('data', data)
    data = [52, 10]

    m = folium.Map(location=data, zoom_start=12, tiles="cartodb positron")


    st.write(data)
#create a map at the chosen location
    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
           ).add_to(m)
    folium_static(m)


    
###################################################################
st.write(' Is this the end?')


p = folium.Map(location=[50, 10], tiles=None, zoom_start=7)
folium.TileLayer("OpenStreetMap").add_to(p)
folium.TileLayer("cartodb positron",show=False).add_to(p)
folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            show=False,
            overlay = False,
            control = True
           ).add_to(p)

folium.TileLayer(
    tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='opentopomap.org',
    show=False,
    ).add_to(p)

# Display the map using Streamlit




# add image
merc = r'\img\1.png' 
if not os.path.isfile(merc):
    st.write(f"Could not find {merc}")

else:
    st.write(f'{merc} found')
    img = folium.raster_layers.ImageOverlay(
        name="Mercator projection SW",
        image=merc,
        bounds=[[51.85, 9.6], [53.3, 11.70]],
        opacity=0.6,
        interactive=True,
        cross_origin=False,
        zindex=1,
    )
    img.add_to(p)






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



folium.LayerControl().add_to(p)


map = st_folium(p, height=800, width=1400)['map']
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


