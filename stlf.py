import os
import folium
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import st_folium
from folium.plugins import Geocoder, ImageOverlay

def prepare_data(selected_subfolder):
    # List all subfolders in the 'img' directory
    subfolders = [f.path for f in os.scandir('img') if f.is_dir()]

    subfolder_path = selected_subfolder

    # Get the list of image names in the selected subfolder
    image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

    # Initialize a DataFrame to store image names, preselect status, and notes
    data = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names), 'Path':['']* len(image_names),'No': list(range(1, len(image_names) + 1)) }

    # Check if 'df' is not in session state, and if not, store it
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame(data)

    return subfolder_path, image_names

def create_map(location):
    return folium.Map(location=location, tiles=None, zoom_start=3)

def add_base_layers(m):
    folium.TileLayer("OpenStreetMap", name='OpenStreetMap').add_to(m)
    folium.TileLayer("cartodb positron", show=False).add_to(m)
    m.add_child(folium.LatLngPopup())
    Geocoder().add_to(m)
    folium.LayerControl().add_to(m)

def get_pos(lat, lng):
    return lat, lng

def map_overview():
    st.write('no location chosen')
    m = create_map(location=[30, 30])
    add_base_layers(m)
    st.write('Choose your general area of interest by clicking')
    map = st_folium(m, height=800, width=1600)

    data = None
    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data)
        st.session_state['loc_chosen'] = data

def map_location_chosen():
    st.write('location chosen')
    p = create_map(location=st.session_state['loc_chosen'])
    add_base_layers(p)

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
    folium.LayerControl().add_to(p)

    return p

def add_image_overlay(p, img_path, bounds=[[51.85, 9.6], [53.3, 11.70]]):
    img_overlay = ImageOverlay(
        name=f"Image",
        image=img_path,
        bounds=bounds,
        opacity=1,
        show=True,
        interactive=False,
        cross_origin=False,
        control=True
    )
    img_overlay.add_to(p)

def add_images_to_sidebar(subfolder_path):
    for i, v in enumerate(st.session_state.df['Image']):
        img_path = os.path.join(subfolder_path, v)

        if st.session_state.df.loc[i, 'Preselect'] == 1:
            add_image_overlay(p, img_path)
            st.session_state.df.loc[i, 'Preselect'] = 0  # Reset preselect status

        img = Image.open(img_path)
        st.sidebar.image(img, use_column_width=True)

        selected = st.sidebar.checkbox(f"Select Image {st.session_state.df.loc[i, 'No']}",
                                       key=f"select
            selected_{st.session_state.df.loc[i, 'No']}", value=st.session_state.df.loc[i, 'Preselect'])
        st.session_state.df.loc[i, 'Preselect'] = int(selected)

    st_folium(p, height=800, width=1400)

def main():
    st.set_page_config(layout="wide")
    st.title("Localizing Aerial Images")

    selected_subfolder = 'img/52N10E'
    subfolder_path, image_names = prepare_data(selected_subfolder)

    # Check if loc_chosen is not in session state, and if not, store it
    if 'loc_chosen' not in st.session_state:
        st.session_state['loc_chosen'] = 0

    # Check if no location is chosen
    if st.session_state['loc_chosen'] == 0:
        map_overview()
    else:
        p = map_location_chosen()
        add_images_to_sidebar(subfolder_path)

if __name__ == "__main__":
    main()
