import base64
import streamlit as st
import gen_wallpaper
import pandas as pd
import json
import os
st.set_option("deprecation.showfileUploaderEncoding", False)

st.markdown("""
# Arknights Desktop Wallpaper Generator

Create desktop wallpapers for your favourite Arknights operators!

Use the download link at the bottom for the best image quality!

You can find the app code on GitHub [here](https://github.com/Ze1598/arknights-desktop-wallpapers).

Feel free to reach out to me on Twitter for feedback [@ze1598](https://twitter.com/ze1598).
""")


def load_data() -> pd.DataFrame:
    data = pd.read_csv("operator_art_dataset.csv")
    # Sort DF by operator name
    data.sort_values(
        ["name", "art_type"], 
        axis="rows",
        ascending=True, 
        inplace=True
    )
    return data


def encode_img_to_b64(img_name: str) -> bytes:
    """Given the name of a image file, load it in bytes mode, and convert it to a base 64 bytes object.
    """
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/19
    with open(img_name, "rb") as f:
        img = f.read()
        encoded_img = base64.b64encode(img).decode()

    return encoded_img


# Load the main DF with all art data
main_data = load_data()

# Dropdown to filter by operator rarity
operator_rank = st.selectbox(
    "Choose the operator rarity",
    ("6-star", "5-star", "4-star", "3-star", "2-star", "1-star")
)

# Filter the data by operator rarity
for star in range(1, 7):
    star = str(star)
    option = star + "-star"
    # Since the dropdown is single-choice only, this will only match a single\
    # rank at any point in time
    if operator_rank == option:
        filtered_data = main_data[main_data["num_stars"] == int(star)]

# Get a subset DF for the filtered rarity
operator_rank_int = int(operator_rank[0])
filtered_data = main_data.query(f"num_stars == {operator_rank_int}")

# Choose the art for the wallpaper
art_chosen = st.selectbox(
    "Choose the operator art for your wallpaper",
    filtered_data["display_name"].to_numpy()
)

# to_dict generates a list of dicts, but we know there will be a single row (dict)
art_chosen_dict = filtered_data[filtered_data["display_name"] == art_chosen].to_dict("records")[0]

# chosen_colour = st.color_picker("Optionally change the background colour")

# Generate the wallpaper and return the file name
wallpaper_name = gen_wallpaper.wallpaper_gen(art_chosen_dict)

# Display the image on the page
st.image(
    wallpaper_name, 
    width=None, 
    use_column_width="auto",
    caption="Wallpaper preview"
)

# Encode the image to bytes so a download link can be created
encoded_img = encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
# Create the download link
st.markdown(href, unsafe_allow_html=True)

# Delete the graphic from the server
os.remove(wallpaper_name)
try:
    os.remove(wallpaper_name)
except:
    pass