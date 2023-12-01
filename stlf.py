import os
import streamlit as st
import pandas as pd
from PIL import Image

# Select a specific subfolder
selected_subfolder = '52N10E'
subfolder_path = os.path.join('img', selected_subfolder)

# Get the list of image names in the selected subfolder
image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

# Initialize a DataFrame to store image names, preselect status, and notes
data = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names)}
df = pd.DataFrame(data)

# Define Streamlit app layout
st.title("Image Selector App")

# Display images in a single column
for i in range(len(df)):
    img_path = os.path.join(subfolder_path, df.loc[i, 'Image'])
    img = Image.open(img_path)
    st.image(img, use_column_width=True, caption=df.loc[i, 'Image'])

    # Checkbox for image selection
    selected = st.checkbox("Select", key=f"select_{i}")
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
