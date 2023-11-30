import streamlit as st
import pandas as pd
import folium
from ast import literal_eval
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder
st.set_page_config(layout="wide")

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
    m = folium.Map(location=[54, 13], zoom_start=1, tiles="cartodb positron",height=900, width=1200,returned_objects=["last_object_clicked"])
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
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data) # Writes to the app
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

st.write(' Is this the end?')








#map = st_folium(m, height=350, width=700)

















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


