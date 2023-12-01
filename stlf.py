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

# Display images in six columns
num_columns = 6
num_images = len(df)

# Calculate the number of rows needed
num_rows = -(-num_images // num_columns)  # Ceiling division

# Display images in a grid layout
for row in range(num_rows):
    col_images = st.columns(num_columns)
    for col in range(num_columns):
        i = row * num_columns + col
        if i < num_images:
            img_path = os.path.join(subfolder_path, df.loc[i, 'Image'])
            img = Image.open(img_path)
            col_images[col].image(img, use_column_width=True, caption=df.loc[i, 'Image'])

            # Checkbox for image selection
            selected = col_images[col].checkbox("Select", key=f"select_{i}")
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

