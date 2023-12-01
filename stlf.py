import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Function to load image names from subfolder into a DataFrame
def load_image_names(subfolder):
    image_names = os.listdir(subfolder)
    df = pd.DataFrame({'Image': image_names, 'preselect': 0, 'notes': ''})
    return df

# Function to display images and handle selection
def display_images(images_df, current_index):
    st.image(images_df.iloc[current_index]['Image'], use_column_width=True, width=90, caption=images_df.iloc[current_index]['Image'])

    # Checkbox for preselecting images
    preselect = st.checkbox('Preselect', value=bool(images_df.iloc[current_index]['preselect']))

    # Save the preselection state
    images_df.at[current_index, 'preselect'] = 1 if preselect else 0

# Main Streamlit app
def main():
    st.title("Image Selection App")

    # List all subfolders in the 'img' directory
    subfolders = [f.path for f in os.scandir('img') if f.is_dir()]

    # Sidebar to select subfolder
    selected_subfolder = st.sidebar.selectbox("Select Subfolder", subfolders)

    # Load images into DataFrame
    images_df = load_image_names(selected_subfolder)

    # Display columns of images
    num_columns = 7
    num_images = len(images_df)
    images_per_column = num_images // num_columns

    for col in range(num_columns):
        start_index = col * images_per_column
        end_index = (col + 1) * images_per_column if col < num_columns - 1 else num_images
        column_images_df = images_df.iloc[start_index:end_index]

        # Display images in this column
        with st.beta_container():
            st.write(f"Column {col + 1}")
            for index, image_row in column_images_df.iterrows():
                display_images(images_df, index)

    # 'Back' and 'Next' buttons
    current_index = st.session_state.get('current_index', 0)
    back_button = st.button("Back")
    next_button = st.button("Next")

    if back_button:
        current_index = max(0, current_index - 1)
    elif next_button:
        current_index = min(num_images - 1, current_index + 1)

    # Save current index in session state
    st.session_state.current_index = current_index

# Run the app
if __name__ == '__main__':
    main()
