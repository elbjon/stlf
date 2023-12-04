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


###########################################
###PREPARATION###
# List all subfolders in the 'img' directory
subfolders = [f.path for f in os.scandir('img') if f.is_dir()]

#st.sidebar.markdown(scrollable_content, unsafe_allow_html=True)
selected_subfolder = 'img/52N10E'

subfolder_path = selected_subfolder #os.path.join('img', selected_subfolder)

# Get the list of image names in the selected subfolder
image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))] # change accordingly

# Initialize a DataFrame to store image names, preselect status, and notes
dada = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names), 'Path':['']* len(image_names),'No': list(range(1, len(image_names) + 1)) }

# Check if 'df' is not in session state, and if not, store it
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame(dada)

# Define Streamlit app layout
st.title("Localizing Aerial Images")
#############################################







# Check if loc_chosen is not in session state, and if not, store it
# Loc_chosen takes the Point of Interest#s coordinates from overview map to detail map. Also the switch from overview to detail map is triggered by it.
if 'loc_chosen' not in st.session_state:
    st.session_state['loc_chosen'] = 0

#Check if no location is chosen
if st.session_state['loc_chosen']==0:
    st.write('no location chosen')
    #Then go for map overview style
    
    # Sidebar Call 1

    # Load and display the image
    image = Image.open('heatmap_Screenshot.png')
    st.sidebar.image(image, caption="Density of Photographic Reconnaissance Flights", use_column_width=True)


    #Main Body Call 1
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
    map = st_folium.map(m,height=800, width=1600,) 

    

    data = None
    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data) # Writes to the app
        #print(f'Is this the correct area? {data}')
        #st.button('next')              

        st.session_state['loc_chosen'] = data


#Call2
#=When loc_chosen is not 0
else:
    st.write('location chosen')
    p = folium.Map(location=st.session_state['loc_chosen'], tiles=None, zoom_start=9)
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




###PREP, originally###

###add images to sidebar
###########################
    for i, v in enumerate(st.session_state.df['Image']):
        #path for sidebar and overlay images
        img_path = os.path.join(subfolder_path, v)        

                    # Create ImageOverlay with a unique name based on counting variable
        if st.session_state.df.loc[i, 'Preselect'] == 1:
            st.write(st.session_state.df.loc[i, 'No'])
            


            img_overlay = folium.raster_layers.ImageOverlay(
            name=f"Image{st.session_state.df.loc[i, 'No']}",
            image=img_path,
            bounds=[[51.85, 9.6], [53.3, 11.70]],  # Adjust the bounds accordingly
            opacity=0.6,
            show=True,
            interactive=False,
            cross_origin=False,
            control=True
            )

            # Add ImageOverlay to the map 'p'
            img_overlay.add_to(p)
            #######################

        
        
        ###actual sidebar images
        #st.session_state.df.loc[i, 'Image'])
        #st.sidebar.markdown(img_path)
        img = Image.open(img_path)#.resize((150, 200))
        
        #save image path into df
        st.session_state.df.loc[i, 'Path']= img_path

        ### Make the whole image a button
        #butt = st.button(st.image(img))
        #st.sidebar.image(butt, use_column_width=True) #, caption='Your Image'
        
        #show image in sidebar

        st.sidebar.image(img, use_column_width=True)

        ### until the whole image is a button run this:
        # Checkbox for image selection in the sidebar
        selected = st.sidebar.checkbox(f"Select Image {st.session_state.df.loc[i, 'No']}", key=f"select_{st.session_state.df.loc[i, 'No']}", value=st.session_state.df.loc[i, 'Preselect'])
        st.session_state.df.loc[i, 'Preselect'] = int(selected)

        #check wether buttons are selected and write state into df
    #####################
        if selected:
            st.session_state.df.loc[i, 'Preselect'] = 1
            #st.write(st.session_state.df.loc[i, 'Image'])




    st_folium.map(p,height=800, width=1400)    

        #else:
        #    st.session_state.df.loc[i, 'Preselect'] = 0
        #col_images[col].image(img, use_column_width=True, caption=st.session_state.df.loc[i, 'Image'])

            # Checkbox for image selection
        #    selected = col_images[col].checkbox("Select", key=f"select_{i}")
            #if selected:
            #   st.session_state.df.loc[i, 'Preselect'] = 1
    #map = st_folium(p, height=800, width=1600)

    #st.write(st.session_state.df)


