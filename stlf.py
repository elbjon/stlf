import os
import streamlit as st
import pandas as pd
from PIL import Image


selected_subfolder = '52N10E'


# Your content that you want to make scrollable
scrollable_content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut porttitor nisl. 
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
Fusce vel lectus vel mauris consequat mattis. Integer fringilla tempus sem, vel bibendum ligula luctus at. 
"""

# List all subfolders in the 'img' directory
subfolders = [f.path for f in os.scandir('img') if f.is_dir()]
st.sidebar.markdown(scrollable_content, unsafe_allow_html=True)
# Select a specific subfolder via sidebar selectbox, for now
#selected_subfolder = st.sidebar("Select Subfolder", scrollable_content)

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

# Number of columns and rows to display
num_columns = 6
num_rows = 3
num_images = len(st.session_state['df'])
num_images_per_page = num_columns * num_rows
num_pages = -(-num_images // num_images_per_page)  # Ceiling division

# Get the current page number from the URL
page_num = int(st.experimental_get_query_params().get("page_num", [0])[0])
st.write(page_num)

# Calculate the start and end indices for the current page
start_index = page_num * num_images_per_page
end_index = min((page_num + 1) * num_images_per_page, num_images)

# Display images in a grid layout
for row in range(num_rows):
    col_images = st.columns(num_columns)
    for col in range(num_columns):
        i = row * num_columns + col + start_index
        if i < end_index:
            img_path = os.path.join(subfolder_path, st.session_state.df.loc[i, 'Image'])
            img = Image.open(img_path).resize((150, 200))
            col_images[col].image(img, use_column_width=True, caption=st.session_state.df.loc[i, 'Image'])

            # Checkbox for image selection
            selected = col_images[col].checkbox("Select", key=f"select_{i}")
            if selected:
                st.session_state.df.loc[i, 'Preselect'] = 1
            #else:
            #    st.session_state.df.loc[i, 'Preselect'] = 0

# Back and Next buttons
back_pressed = st.button("Back")
next_pressed = st.button("Next")

# Handle button clicks
if back_pressed:
    new_page_num = max(0, page_num - 1)
    st.experimental_set_query_params(page_num=new_page_num)
    st.write("Back button clicked")

if next_pressed:
    new_page_num = min(num_pages - 1, page_num + 1)
    st.experimental_set_query_params(page_num=new_page_num)
    st.write("Next button clicked")

# Display the DataFrame (optional, for debugging)
st.write(st.session_state.df)
