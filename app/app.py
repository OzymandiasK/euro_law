import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd


def main():
    st.title("European Freelancer Fiscal Laws Map")

    # Load GeoJSON data
    europe_map = gpd.read_file("app/europe.geojson")

    # Initialize the map
    map_center = [54.5260, 15.2551]  # Approximate center of Europe
    folium_map = folium.Map(location=map_center, zoom_start=4)

    # Optionally, add markers or other layers based on your data
    # For simplicity, this is skipped here

    # Display the map in Streamlit
    folium_static(folium_map)


if __name__ == "__main__":
    main()
