from typing import final
import pandas as pd

# Load CSV with operator info and elite art
elite_df = pd.read_csv("https://raw.githubusercontent.com/Ze1598/arknights-wallpaper-generator/main/static/data/operators_info.csv")
# Remove unwanted columns
elite_df = elite_df.drop(["has_e2", "color"], axis="columns")
# Unpivot the art columns to have one with the art type and another with the url
elite_df = elite_df.melt(
    id_vars=["name", "num_stars"], 
    value_vars=["e0_img", "e2_img"],
    var_name="art_type",
    value_name="art_url"
)

# Load JSON with skin art
skin_df = pd.read_json("https://raw.githubusercontent.com/Ze1598/arknights-wallpaper-generator/main/static/data/skins_info.json")
# Transpose DF to use names as index
skin_df = skin_df.transpose()
# Reset index to use the names as another column
skin_df = skin_df.reset_index().rename(columns={"index": "name"})
# Unpivot the art columns to have one with the art type and another with the url
skin_df = skin_df.melt(
    id_vars=["name"],
    var_name="art_type",
    value_name="art_url"
)

# Final DF with data from both sources
final_df = elite_df.append(skin_df)
# Remove rows without art url
final_df = final_df.dropna(axis="rows", subset=["art_url"])
# Sort by name, then by rarity (desc), so each operator shows first the rows with rarity (rows from the skins source doesn't have rarity)
final_df = final_df.sort_values(["name", "num_stars"], axis="rows", ascending=False)
# Fill down rarity for the skin rows
final_df = final_df.ffill(axis="rows")
# Clean up art type names
final_df["art_type"] = final_df["art_type"].map(
    lambda art_type:
        "Elite 2" if art_type == "e2_img"
        else "Elite 1" if art_type == "E1 art"
        else "Elite 0" if art_type == "e0_img"
        else art_type
)
print(final_df)
print(final_df.columns)
final_df.to_csv("operator_art_dataset.csv", index=False)