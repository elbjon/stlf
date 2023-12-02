import os
import streamlit as st
import pandas as pd
from PIL import Image


#selected_subfolder = '52N10E'

# List all subfolders in the 'img' directory
subfolders = [f.path for f in os.scandir('img') if f.is_dir()]

# Select a specific subfolder
selected_subfolder = st.sidebar.selectbox("Select Subfolder", subfolders)

subfolder_path = os.path.join('img', selected_subfolder)



# Get the list of image names in the selected subfolder
image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

# Initialize a DataFrame to store image names, preselect status, and notes
data = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names)}


# Check if 'df' is not in session state, and if not, store it
if 'df' not in st.session_state:
    df = pd.DataFrame(data)
    st.session_state.df = df

# Define Streamlit app layout
st.title("Image Selector App")

# Number of columns and rows to display
num_columns = 6
num_rows = 4
num_images = len(st.session_state.df)
num_images_per_page = num_columns * num_rows
num_pages = -(-num_images // num_images_per_page)  # Ceiling division

# Get the current page number from the URL
page_num = int(st.experimental_get_query_params().get("page_num", [0])[0])

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
