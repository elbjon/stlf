import os
import folium
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import st_folium, folium_static
from folium.plugins import Draw
from folium.plugins import Geocoder


#set layout to wide
st.set_page_config(layout="wide")

# Check if loc_chosen is not in session state, and if not, store it
# Loc_chosen takes the Point of Interest#s coordinates from overview map to detail map. Also the switch from overview to detail map is triggered by it.
if 'loc_chosen' not in st.session_state:
    st.session_state['loc_chosen'] = 0

#Check if no location is chosen
if st.session_state['loc_chosen']==0:
    #Then go for overview map
    
    # Sidebar
    # Image file path
    image_path = "images/example_image.png"

    # Load and display the image
    image = Image.open('heatmap_Screenshot.png')
    st.sidebar.image(image, caption="Density of Photographic Reconnaissance Flights", use_column_width=True)


    #Main Body
    def get_pos(lat, lng):
        return lat, lng

    m = folium.Map(location=[30, 30], tiles=None, zoom_start=3)
    folium.TileLayer("OpenStreetMap", name= 'OpenStreetMap').add_to(m)
    folium.TileLayer("cartodb positron",show=False).add_to(m)
    
    m.add_child(folium.LatLngPopup())
    
    # add search field
    Geocoder().add_to(m)

    folium.LayerControl().add_to(m)

    st.write('Choose your general area of interest by clicking')
    map = st_folium(m,height=800, width=1600,) 

    

    data = None
    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data) # Writes to the app
        #print(f'Is this the correct area? {data}')
        #st.button('next')              

        st.session_state['loc_chosen'] = data


#=When loc_chosen is not 0
else:
    p = folium.Map(location=[52.5, 10.5], tiles=None, zoom_start=9)
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

    # add search field
    Geocoder().add_to(p)

    folium.LayerControl().add_to(p)


    map = st_folium(p, height=800, width=1600)


    # List all subfolders in the 'img' directory
    subfolders = [f.path for f in os.scandir('img') if f.is_dir()]


    






























    #st.sidebar.markdown(scrollable_content, unsafe_allow_html=True)
    selected_subfolder = 'img/52N10E'

    subfolder_path = selected_subfolder #os.path.join('img', selected_subfolder)



    # Get the list of image names in the selected subfolder
    image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))] # change accordingly

    # Initialize a DataFrame to store image names, preselect status, and notes
    data = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names)}








    # Check if 'df' is not in session state, and if not, store it
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame(data)

    # Define Streamlit app layout
    st.title("Part 2: Image Selector App")


    for i, v in enumerate(st.session_state.df['Image']):

        img_path = os.path.join(subfolder_path, v)#st.session_state.df.loc[i, 'Image'])
        #st.sidebar.markdown(img_path)
        img = Image.open(img_path)#.resize((150, 200))
        
        
        ### Make the whole image a button
        #butt = st.button(st.image(img))
        #st.sidebar.image(butt, use_column_width=True) #, caption='Your Image'
        
        
        st.sidebar.image(img, use_column_width=True)

        ### until the whole image is a button:
        # Checkbox for image selection in the sidebar
        selected = st.sidebar.checkbox(f"Select Image {i}", key=f"select_{i}", value=st.session_state.df.loc[i, 'Preselect'])
        st.session_state.df.loc[i, 'Preselect'] = int(selected)



        if selected:
            st.session_state.df.loc[i, 'Preselect'] = 1
            st.write(st.session_state.df.loc[i, 'Image'])




        #else:
        #    st.session_state.df.loc[i, 'Preselect'] = 0
        #col_images[col].image(img, use_column_width=True, caption=st.session_state.df.loc[i, 'Image'])

            # Checkbox for image selection
        #    selected = col_images[col].checkbox("Select", key=f"select_{i}")
            #if selected:
            #   st.session_state.df.loc[i, 'Preselect'] = 1

    st.write(st.session_state.df)

