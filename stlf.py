import os
import folium
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder

def prepare_data(selected_subfolder):


    subfolder_path = selected_subfolder

    # Get the list of image names in the selected subfolder
    image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

    # Initialize a DataFrame to store image names, preselect status, and notes
    data1 = {'Image': image_names, 'Preselect': [0] * len(image_names),  'Preselect_2': [0] * len(image_names), 'Note': [''] * len(image_names), 'Path':['']* len(image_names),'No': list(range(1, len(image_names) + 1)) }

    # Check if 'df' is not in session state, and if not, store it
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame(data1)

    return subfolder_path, image_names

def create_map(location):
    return folium.Map(location=location, tiles=None, zoom_start=3)




def get_pos(lat, lng):
    return lat, lng

def map_overview():

    ###sidebar
    # Load and display the image
    image = Image.open('heatmap_Screenshot.png')
    st.sidebar.image(image, caption="Density of Photographic Reconnaissance Flights", use_column_width=True)


    ###body
    st.write('no location chosen')
    m = create_map(location=[30, 30])

    folium.TileLayer("OpenStreetMap", name='OpenStreetMap').add_to(m)
    folium.TileLayer("cartodb positron", show=False).add_to(m)
    m.add_child(folium.LatLngPopup())
    Geocoder().add_to(m)
    folium.LayerControl().add_to(m)


    st.write('Choose your area of interest by clicking')
    map = st_folium(m, height=800, width=1400)

    data = None
    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data)
        st.session_state['loc_chosen'] = data



def map_detail(subfolder_path):
    st.write('location chosen')
    p = create_map(location=st.session_state['loc_chosen'])
    folium.TileLayer("OpenStreetMap", name='OpenStreetMap').add_to(p)
    folium.TileLayer("cartodb positron", show=False).add_to(p)
    
    

    # Add additional layers as needed
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite Image',
        show=False,
        overlay=False,
        control=True
    ).add_to(p)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        name='Topographic Map',
        attr='opentopomap.org',
        show=False,
    ).add_to(p)

    Geocoder().add_to(p)


#overlays
#################################################
    # smaller df
    
    sel_df = st.session_state.df[st.session_state.df['Preselect'] == 1 | (st.session_state.df['Preselect_2'] == 1)].copy()
    sel_df = sel_df.reset_index()

    

    #create/clean list of previous overlays
    prev_overlays_list=[]
    for i, v in enumerate(sel_df['Image']):
        #I cannot put this in a function because it wouldn't work anymore then. This are the restrictions of Streamlit and Folium 
    
        #st.write(i)
        #st.write(sel_df.loc[i, 'Preselect_2'])
        name_no = sel_df.loc[i, 'No']

        if sel_df.loc[i, 'Preselect_2']==0:
            img_path = os.path.join(subfolder_path, v)
            


            bounds=[[st.session_state['loc_chosen'][0]-0.15,st.session_state['loc_chosen'][1]-0.4],[st.session_state['loc_chosen'][0]+1.3,st.session_state['loc_chosen'][1]+1.7]]
            #st.write(str(bounds))
            img_overlay = folium.raster_layers.ImageOverlay(
            name=f"BILDS {name_no}",
            image=img_path,
            bounds=bounds,
            opacity=0.6,
            show=True,
            interactive=False,
            cross_origin=False,
            control=True
            )
            img_overlay.add_to(p)

        else:
            #st.write('preselect != 0')
            
            
            
            img_path = os.path.join(subfolder_path, v)
            
            bounds=[[st.session_state['loc_chosen'][0]-0.15,st.session_state['loc_chosen'][1]-0.4],[st.session_state['loc_chosen'][0]+1.3,st.session_state['loc_chosen'][1]+1.7]]
            #st.write(str(bounds))
            img_overlay = folium.raster_layers.ImageOverlay(
                name=f"Image {name_no}",
                image=img_path,
                bounds=bounds,
                opacity=0.6,
                show=False,
                interactive=False,
                cross_origin=False,
                control=True
                )
            #add layer to layergroup

            #add layer to layer list
            prev_overlays_list.append(img_overlay)





        #add layers from layerlist to map
        if prev_overlays_list != []:
            #st.write('list is not empty')
            for overlay in prev_overlays_list:
                #st.write(overlay)
                overlay.add_to(p)




    st.session_state.df.loc[:, 'Preselect_2'] = st.session_state.df['Preselect'].values

    # try to deselect
    st.session_state.df.loc[st.session_state.df['Preselect'] == 1, 'Preselect'] = 0
    
    #print from df where sel_df, print name/name_No and URL to original jpeg ####BUT NOW START WITH IMAG PROCESSING!!!
    st.write(sel_df) 
################################################


    #add layer control box
    folium.LayerControl().add_to(p)

    #show map, USE folium_static, st_folium not working!!!
    folium_static(p, height=800, width=1400)

    

    # no return needed, map printing done here. delete return when everything is running
    return p


def populate_side(subfolder_path):

        # Add images to sidebar
        for i, v in enumerate(st.session_state.df['Image']):
            img_path = os.path.join(subfolder_path, v)

            

            img = Image.open(img_path)
            st.sidebar.image(img, use_column_width=True)

            selected = st.sidebar.checkbox(f"Select Image {st.session_state.df.loc[i, 'No']}", key=f"select selected_{st.session_state.df.loc[i, 'No']}", value=st.session_state.df.loc[i, 'Preselect'])
            st.session_state.df.loc[i, 'Preselect'] = int(selected)
            
            #if st.session_state.df.loc[i, 'Preselect'] == 1:
                #add_image_overlay(p, img_path)
                #st.write('now add image overlay would have been called in populate_side()')
                
                #st.session_state.df.loc[i, 'Preselect'] = 0  # Reset preselect status

##########################

###############################





def add_image_overlay(p, img_path):
    st.write(img_path)
    bounds=[[st.session_state['loc_chosen'][0]-0.15,st.session_state['loc_chosen'][1]-0.4],[st.session_state['loc_chosen'][0]+1.3,st.session_state['loc_chosen'][1]+1.7]]
    st.write(str(bounds))
    img_overlay = folium.raster_layers.ImageOverlay(
        name=f"Image",
        image=img_path,
        bounds=bounds,
        opacity=0.6,
        show=True,
        interactive=False,
        cross_origin=False,
        control=True
    )
    img_overlay.add_to(p)

def main():
    st.set_page_config(layout="wide")
    st.title("Localizing Aerial Images")
    

    selected_subfolder = 'img/52N13E' #you know what to do
    subfolder_path, image_names = prepare_data(selected_subfolder)

        # List all subfolders in the 'img' directory
    #subfolders = [f.path for f in os.scandir('img') if f.is_dir()]


    # Check if loc_chosen is not in session state, and if not, store it
    if 'loc_chosen' not in st.session_state:
        st.session_state['loc_chosen'] = 0

    # Check if no location is chosen
    if st.session_state['loc_chosen'] == 0:
        map_overview()
    else:
        populate_side(subfolder_path)
        map_detail(subfolder_path) #this is p which was used to call populate_side()
        
        
        

        ###########
       


        

if __name__ == "__main__":
    main()
