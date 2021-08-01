from PIL import Image
from colorthief import ColorThief
import requests
from io import BytesIO
from typing import List, Tuple
from requests.models import Response
import pandas as pd
import os


def request_image(url: str) -> Response:
    res = requests.get(url)
    return res


def get_colour_palette(res: Response) -> List[Tuple[int]]:
    # Load the image as binary data (contents of the request's response)
    img_bytes = BytesIO(res.content)

    colour_thief = ColorThief(img_bytes)
    # Build a colour palette
    palette = colour_thief.get_palette(color_count=6)

    return palette


def prepare_op_art(res: Response) -> any:
    op_art = Image\
        .open(BytesIO(res.content), mode="r")\
        .convert("RGBA")\
        .resize((1382, 1382))

    return op_art


if __name__ == "__main__":
    ART_COORD = (700, 0)
    SHADOW_OFFSET = (10, 10)
    SHADOW_COORD = tuple(ART_COORD[i] + SHADOW_OFFSET[i] for i in range(len(ART_COORD)))

    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2020-08/char_172_svrash_summer%234.png"
    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2019-11/char_103_angel_2.png"
    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2020-02/ArtExuSkinKFC.png"
    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2020-10/char_250_phatom_ghost%231.png"
    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2019-11/char_172_svrash_2.png"
    # operator = "https://gamepress.gg/arknights/sites/arknights/files/2020-08/char_2013_cerber_summer%234.png"

    data = pd.read_csv("operator_art_dataset.csv")
    for operator_row in data.iterrows():
        # iterrows returns a tuple (index, row_series)
        operator_data = operator_row[1]
        wallpaper_name = f"{operator_data[0]}_{operator_data[2]}.png"
        wallpaper_path = os.path.join(os.getcwd(), "wallpapers", wallpaper_name)

        print("Creating", wallpaper_name)

        # Request the operator art
        img_res = request_image(operator_data[3])
        # Generate a colour pallette based on the most dominant colours
        palette = get_colour_palette(img_res)
        main_colour = palette[0]
        op_art = prepare_op_art(img_res)

        wallpaper = Image.new("RGBA", (1920, 1080), color=main_colour)

        shadow = Image.new("RGBA", op_art.size, color="black")
        wallpaper.paste(shadow, SHADOW_COORD, mask=op_art)
        
        wallpaper.paste(op_art, ART_COORD, mask=op_art)

        wallpaper.save(wallpaper_path)
