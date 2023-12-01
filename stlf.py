import os
import streamlit as st
import pandas as pd
from PIL import Image

# Function to get image names from a subfolder
def get_image_names(subfolder):
    subfolder_path = os.path.join('img', subfolder)
    if os.path.exists(subfolder_path):
        return [f for f in os.listdir(subfolder_path) if f.endswith('.jpg')]
    return []

# Function to display images and handle selection
def display_images(subfolder, images):
    st.header(f"Images in {subfolder}")
    df = pd.DataFrame({'Image': images, 'Preselect': [0] * len(images), 'Notes': [''] * len(images)})

    for i, row in df.iterrows():
        image_path = os.path.join('img', subfolder, row['Image'])
        img = Image.open(image_path)
        st.image(img, caption=row['Image'], width=60, use_column_width=False)
        
        # Checkbox to preselect
        row['Preselect'] = st.checkbox(f"Preselect {i+1}", key=f"checkbox_{i}")

        # Text input for notes
        row['Notes'] = st.text_input(f"Notes {i+1}")

    st.write(df)

# Main Streamlit app
def main():
    st.title("Image Selection App")

    # Get a list of subfolders in the 'img' directory
    subfolders = [f for f in os.listdir('img') if os.path.isdir(os.path.join('img', f))]

    # Dropdown to select a subfolder
    selected_subfolder = st.sidebar.selectbox("Select Subfolder", subfolders)

    # Get image names from the selected subfolder
    images = get_image_names(selected_subfolder)

    # Display images and handle selection
    display_images(selected_subfolder, images)

if __name__ == "__main__":
    main()
