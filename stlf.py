import os
import folium
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder
### Erledigen:
### change to one map!!!! Make the overlay stuff a function on its own. ### no, let it as it is
### keep zoom and map focus when (re)loading a map
### GEOLOCATION!!! Äquator, Pol, einer dazwischen? dazwischen prozentual angleichen 
### DONE: program logic
### load and process real data, not exemplary images (two steps? 1 all preprocessed images, 2. load and preprocess new images)
### Detailkarte scheint neu geladen zu werden, wenn ein anderer Overlay ausgewählt wird (muss das sein? kann man nicht elemente zu Karte hinzufügen [wohl nicht] oder Elemente schon auf Karte laden, aber nicht anzeigen (weder overlay control noch als overlay selbst...)) 
### Werden die Bilder in der Sidebar komplett neu geladen bei Auswahl eines Bildes? Vergleichen mit Aufruf von populate und detailmap in overviewmap


#vorherige to do liste:
    ##change program logic, main()... 
    
    #Replace dependency from loc_chosen with call of next function after map clicking/(Button click?)
    #Check wether folder exists
    #calculate offset/do new geo-referencing matching to all longitudes, measurements for offset at equator and close to one pole, then divide by number of longitudes effected. Et Voila-> offset for each longitude!


def prepare_data(selected_subfolder):

    #temporär. Mache Abfrage, ob Subfolder exists, else look for info (existance plus download links) in main dataframe(the one not used yet in this program)
    #download and process and store images (ggfs in batches...) ##look for nice work in progress bar or the like in streamlit
    #ggfs. Fehlermeldung-> Try again.
    subfolder_path = selected_subfolder

    # Get the list of image names in the selected subfolder
    image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

    # Initialize a DataFrame to store image names, preselect status, and notes
    data1 = {'Image': image_names, 'Preselect': [0] * len(image_names),  'Preselect_2': [0] * len(image_names), 'Note': [''] * len(image_names), 'Path':['']* len(image_names),'No': list(range(1, len(image_names) + 1)) }
    # Add a 'URL' column with the specified format
    

    # Check if 'df' is not in session state, and if not, store it
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame(data1)
        st.session_state.df['URL'] = st.session_state.df.apply(lambda row: f'<a href="https://www.Image.com">{row["Image"]}\'{row["No"]}</a>', axis=1)
        #st.write(st.session_state.df)
        #st.dataframe(st.session_state.df.style.format({'URL': lambda x: f'<a href="{x}">{x}</a>'}), unsafe_allow_html=True)
    return subfolder_path, image_names


def create_map(location):
    return folium.Map(location=location, tiles=None, zoom_start=3)

    #makes lat lng easy reading tuple data
def get_pos(lat, lng):
    return lat, lng

def zeropoint_coord(data):
    #return_data = []
    return_string ='' #subfolder

    ########### Wo bleiben Eleganz und Effizienz?
    for i, v in enumerate(data):
        if v >= 0:
            return_string = return_string + str(int(v))
            if i==0: 
                return_string = return_string +'N_'
            else:
                return_string = return_string +'W_'
        else:
            return_string = return_string + str(int(v*-1))
            if i==0: 
                return_string = return_string +'S'
            else:
                return_string = return_string +'E'
    st.write(return_string)


def map_overview():
    ###sidebar
    # Load and display the sidebar image
    image = Image.open('heatmap_Screenshot.png')
    st.sidebar.image(image, caption="Density of Photographic Reconnaissance Flights", use_column_width=True)

    ###body
    #create map object via call map method
    m = create_map(location=[30, 30])

    #add attributes to the map: Layers, popup, adress search, layercontrol
    folium.TileLayer("OpenStreetMap", name='OpenStreetMap').add_to(m)
    folium.TileLayer("cartodb positron", show=False).add_to(m)
    m.add_child(folium.LatLngPopup())
    Geocoder().add_to(m)
    folium.LayerControl().add_to(m)

    st.write('Choose your area of interest by clicking')
    # show map
    map = st_folium(m, height=800, width=1400) 
    #st.write(folium.Map)
    st.write(map,'test1')
    #st.write('test2', map.get_bounds(map))    
    #data = None
    #das geht schöner...
    if map.get("last_clicked"):
        
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
        st.session_state['loc_chosen'] = data
        #st.write('session state:, ',  st.session_state['loc_chosen'])
        #st.write('session state length:, ',  len(st.session_state['loc_chosen']))
        #st.write('map clicked_1', data)
        
        #prepare data first:
        subfolder_path = r'USA_A_F_Step_2/38N_46E' #'img/52N13E' #you know what to do "C:\Users\Administrator\Documents\GitHub\stlf\USA_A_F_Step_2\38N_46E"


 
        #############
########Start prepare_data() and map_detail() here!!! (and add a back button or ask if location is okay)
        #############
        #baba = (map["last_clicked"]["lat"], map["last_clicked"]["lng"])
        zeropoint_coord(data)
        



### Delete after testing new position        
#    if 'loc_chosen' in st.session_state:
#        #st.write('loc_chosen is not None', len(st.session_state['loc_chosen']))
#        #st.write(st.session_state['loc_chosen'], 'test')
#        populate_side(subfolder_path)
#        map_detail(subfolder_path)




       


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


    #folium.Marker(
    #    [38,46], popup="38,46", tooltip="HELLOHELLO"
    #).add_to(p)
    #folium.Marker(
    #    [39, 46], popup="39, 46", tooltip="HELLOHELLO"
    #).add_to(p)
    #folium.Marker(
    #    [39, 47], popup="39, 47", tooltip="HELLOHELLO"
    #).add_to(p)
    #folium.Marker(
    #    [38, 47], popup="38, 47", tooltip="HELLOHELLO"
    #).add_to(p)


    Geocoder().add_to(p)

#overlays
#################################################
    # smaller df    
    sel_df = st.session_state.df[st.session_state.df['Preselect'] == 1 | (st.session_state.df['Preselect_2'] == 1)].copy()
    sel_df = sel_df.reset_index()    

    #create/clean list of previous overlays
    prev_overlays_list=[]
    for i, v in enumerate(sel_df['Image']):
        #I cannot put this into a function because it wouldn't work anymore due to the restrictions of Streamlit and Folium 
    
        #st.write(i)
        #st.write(sel_df.loc[i, 'Preselect_2'])
        name_no = sel_df.loc[i, 'No']

        if sel_df.loc[i, 'Preselect_2']==0:
            img_path = os.path.join(subfolder_path, v)

            ###This was just thought as a quick temporary solution. It cannot work as the degre squares have different sizes. Larger at the equator, the smallest at the poles
            bounds=[[st.session_state['loc_chosen'][0]-0.25,st.session_state['loc_chosen'][1]-0.95],[st.session_state['loc_chosen'][0]+0.95,st.session_state['loc_chosen'][1]+1.05]]
            #st.write(str(bounds))
            img_overlay = folium.raster_layers.ImageOverlay(
            name=f"Current Image {name_no}",
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
            
            bounds=[[st.session_state['loc_chosen'][0]-0.25,st.session_state['loc_chosen'][1]-0.95],[st.session_state['loc_chosen'][0]+0.95,st.session_state['loc_chosen'][1]+1.05]]
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
    
   

################################################


    #add layer control box
    folium.LayerControl().add_to(p)

    #make map look alike to the overview map 
    p.fit_bounds([[0, 0], [10, 10]])

    #show map, USE folium_static, st_folium not working!!!
    pap = folium_static(p, height=800, width=1400)
    st.write(pap)

#print from df where sel_df, print name/name_No and URL to original jpeg ####BUT NOW START WITH IMAG PROCESSING!!!
    #st.write(sel_df)


#ÖÖÖÖÖÖÖÖÖÖÖ MAKE A loop

    # Iterate through the DataFrame
    for index, row in sel_df.iterrows():
    # Print values from multiple columns
    #print(f"Row {index + 1}: Column1 = {row['Column1']}, Column2 = {row['Column2']}, Column3 = {row['Column3']}")
    
    
        st.markdown( f"[Image No {row['No']}_URL](www.url.com)")
    


    # no return needed, map plotting done here. delete return when everything is running
    return p


def populate_side(subfolder_path):
    if st.session_state['button_clicked'] == 0:

        
        if st.sidebar.button('if location is correct, click here for loading the images', type="primary"):
            st.session_state['button_clicked'] = 1
            st.sidebar.write('loading...')
        else:
            st.sidebar.write('click at a location on the map, then hit the button')
        
    if st.session_state['button_clicked'] == 1:
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




#just keepin' it as a reminder that a function would be nicer
def add_image_overlay(p, img_path):
    st.write(img_path)
    bounds=[[st.session_state['loc_chosen'][0]-0.15,st.session_state['loc_chosen'][1]-0.85],[st.session_state['loc_chosen'][0]+1.3,st.session_state['loc_chosen'][1]+1.25]]
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

    #streamlit page configuration
    st.set_page_config(layout="wide")
    st.title("Aerial Image Search")

    #set initial variable states:
    if 'button_clicked' not in st.session_state: 
        st.session_state['button_clicked'] = 0


    #select subfolder. Not here. Move to method...
    selected_subfolder = r'USA_A_F_Step_2/38N_46E' #'img/52N13E' #you know what to do "C:\Users\Administrator\Documents\GitHub\stlf\USA_A_F_Step_2\38N_46E"
    subfolder_path, image_names = prepare_data(selected_subfolder)
    #prepare_data(selected_subfolder)
    subfolder_path = selected_subfolder

    ### Delete after testing new position        
    if 'loc_chosen' in st.session_state:
#        #st.write('loc_chosen is not None', len(st.session_state['loc_chosen']))
#        #st.write(st.session_state['loc_chosen'], 'test')
        populate_side(subfolder_path) ### sollte nicht jedesmal bilder neu laden!
        map_detail(subfolder_path)
    else:
        map_overview()

### old logic:
#    # Check if loc_chosen is not in session state, and if not, store it
#    if 'loc_chosen' not in st.session_state:
#        st.session_state['loc_chosen'] = 0
#
#    # Check if no location is chosen
#    if st.session_state['loc_chosen'] == 0:
#        
#    else:
#        populate_side(subfolder_path)
#        map_detail(subfolder_path) #this is p which was used to call populate_side()
        
        ###########  


if __name__ == "__main__":
    main()
