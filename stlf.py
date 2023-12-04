import os
import streamlit as st
import pandas as pd
from PIL import Image





# Your content that you want to make scrollable
scrollable_content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut porttitor nisl. 
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
Fusce vel lectus vel mauris consequat mattis. Integer fringilla tempus sem, vel bibendum ligula luctus at. 
"""

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
    
    st.sidebar.image(img, caption='Your Image', use_column_width=True)

    # Checkbox for image selection in the sidebar
    selected = st.sidebar.checkbox(f"Select Image {i}", key=f"select_{i}", value=st.session_state.df.loc[i, 'Preselect'])
    st.session_state.df.loc[i, 'Preselect'] = int(selected)


    
    if selected:
        st.session_state.df.loc[i, 'Preselect'] = 1
    #else:
    #    st.session_state.df.loc[i, 'Preselect'] = 0
    #col_images[col].image(img, use_column_width=True, caption=st.session_state.df.loc[i, 'Image'])

        # Checkbox for image selection
    #    selected = col_images[col].checkbox("Select", key=f"select_{i}")
        #if selected:
         #   st.session_state.df.loc[i, 'Preselect'] = 1

