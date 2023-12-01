import os
import streamlit as st
import pandas as pd
from PIL import Image

# Define the path to the image folder
repo_path = 'path/to/your/github/repo'
img_folder = os.path.join(repo_path, 'img')

# Get a list of subfolders in the img directory
subfolders = [f.name for f in os.scandir(img_folder) if f.is_dir()]

# Initialize a DataFrame to store image names, preselect status, and notes
data = {'Image': [], 'Preselect': [], 'Note': []}
df = pd.DataFrame(data)

# Populate the DataFrame with image names from subfolders
for subfolder in subfolders:
    subfolder_path = os.path.join(img_folder, subfolder)
    image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]
    df = pd.concat([df, pd.DataFrame({'Image': image_names, 'Preselect': 0, 'Note': ''})], ignore_index=True)

# Define Streamlit app layout
st.title("Image Selector App")

# Display images in seven columns
columns = st.beta_columns(7)
for i, col in enumerate(columns):
    if i < len(df):
        img_path = os.path.join(img_folder, df.loc[i, 'Image'])
        img = Image.open(img_path)
        col.image(img, use_column_width=True, caption=df.loc[i, 'Image'])

        # Checkbox for image selection
        selected = col.checkbox("Select", key=f"select_{i}")
        if selected:
            df.loc[i, 'Preselect'] = 1
        else:
            df.loc[i, 'Preselect'] = 0

# Back and Next buttons
back_pressed = st.button("Back")
next_pressed = st.button("Next")

# Handle button clicks
if back_pressed:
    st.write("Back button clicked")
    # Add logic to go back to the previous set of images

if next_pressed:
    st.write("Next button clicked")
    # Add logic to go to the next set of images

# Display the DataFrame (optional, for debugging)
st.write(df)
