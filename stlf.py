import os
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

# Function to get the session state
def get_session_state():
    ctx = get_report_ctx()
    this_session = None
    current_server = Server.get_current()

    if hasattr(current_server, '_session_infos'):
        # Streamlit < 1.10
        session_infos = current_server._session_infos.values()
    else:
        # Streamlit >= 1.10
        session_infos = current_server.session_state.session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            this_session = session_info.session
            break

    if this_session is None:
        raise RuntimeError("Couldn't get Streamlit session.")

    if not hasattr(this_session, '_custom_session_state'):
        this_session._custom_session_state = CustomSessionState()

    return this_session._custom_session_state

# Custom Session State class
class CustomSessionState:
    def __init__(self):
        self.page_num = 0

# Select a specific subfolder
selected_subfolder = '52N10E'
subfolder_path = os.path.join('img', selected_subfolder)

# Get the list of image names in the selected subfolder
image_names = [f.name for f in os.scandir(subfolder_path) if f.is_file() and f.name.endswith(('.jpg', '.png'))]

# Initialize a DataFrame to store image names, preselect status, and notes
data = {'Image': image_names, 'Preselect': [0] * len(image_names), 'Note': [''] * len(image_names)}
df = pd.DataFrame(data)

# Get session state
session_state = get_session_state()

# Define Streamlit app layout
st.title("Image Selector App")

# Number of columns and rows to display
num_columns = 10
num_rows_per_page = 2
num_images = len(df)
num_pages = -(-num_images // (num_columns * num_rows_per_page))  # Ceiling division

# Calculate the start and end indices for the current page
start_index = session_state.page_num * num_columns * num_rows_per_page
end_index = min((session_state.page_num + 1) * num_columns * num_rows_per_page, num_images)

# Display images in a grid layout
for row in range(num_rows_per_page):
    col_images = st.columns(num_columns)
    for col in range(num_columns):
        i = row * num_columns + col + start_index
        if i < end_index:
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
    if session_state.page_num > 0:
        session_state.page_num -= 1
    st.write("Back button clicked")

if next_pressed:
    if session_state.page_num < num_pages - 1:
        session_state.page_num += 1
    st.write("Next button clicked")

# Display the DataFrame (optional, for debugging)
st.write(df)
