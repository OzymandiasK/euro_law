import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import branca.colormap as cm  # Import the cm module
import os


def main():
    st.title("European Freelancer Fiscal Laws Map")

    # Load the Excel data into a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "Fiscal_data_EU.xlsx")
    excel_data = pd.read_excel(data_path)
    excel_data["Tax Rate"] = pd.to_numeric(excel_data["Tax Rate"], errors="coerce")

    # Ensure the GeoJSON file is read into a GeoDataFrame
    europe_geojson = gpd.read_file("/app/europe.geojson")

    # Merge the Excel DataFrame with the GeoDataFrame based on the country name
    merged_data = gpd.GeoDataFrame(
        europe_geojson.merge(excel_data, left_on="name", right_on="Country")
    )

    linear = cm.LinearColormap(
        ["green", "yellow", "red"],
        vmin=excel_data["Tax Rate"].min(),
        vmax=excel_data["Tax Rate"].max(),
    )

    # Create a Folium map
    folium_map = folium.Map(location=[54.5260, 15.2551], zoom_start=4)

    # Add a simple tooltip with country name and tax rate
    tooltip = folium.features.GeoJsonTooltip(
        fields=["name", "Tax Rate", "Specificities"],
        aliases=["Country", "Tax Rate", "Specificities"],
        sticky=False,
    )

    def style_function(feature):
        tax_rate = feature["properties"]["Tax Rate"]
        return {
            "fillColor": linear(tax_rate),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.7,
        }

    # Add the merged data as a GeoJSON layer to the map with the tooltip
    folium.GeoJson(
        data=merged_data,
        style_function=style_function,
        name="Tax Rate (%)",
        highlight_function=lambda x: (
            {"weight": 3, "fillOpacity": 0.9}
            if x["type"] == "Feature"
            else {"weight": 3, "fillOpacity": 0.9}
        ),
        tooltip=tooltip,
    ).add_to(folium_map)

    folium_static(folium_map, width=1250, height=900)

    # Display the source links as clickable URLs
    for _, row in excel_data.iterrows():
        st.write(f"[{row['Country']}]({row['Source']})")


if __name__ == "__main__":
    main()
