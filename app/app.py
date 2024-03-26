import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import branca.colormap as cm
import os

# Set page config
st.set_page_config(
    page_title="EU Freelancer Fiscal Map",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Function to load data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "Fiscal_data_EU.xlsx")
    geojson_path = os.path.join(current_dir, "europe.geojson")

    excel_data = pd.read_excel(data_path)
    excel_data["Tax Rate"] = pd.to_numeric(excel_data["Tax Rate"], errors="coerce")
    europe_geojson = gpd.read_file(geojson_path)

    return excel_data, europe_geojson


def main():
    st.title("IT Freelancer - Fiscal Map")
    st.markdown(
        "Explore the fiscal laws and tax rates for freelancers across Europe. Select a country from the sidebar for more details!"
    )

    excel_data, europe_geojson = load_data()

    # Sidebar
    with st.sidebar:
        st.header("Country Details")
        selected_country = st.selectbox(
            "Select a country:", sorted(excel_data["Country"].unique())
        )
        country_info = excel_data[excel_data["Country"] == selected_country].iloc[0]
        st.markdown(f"**Tax Rate:** {country_info['Tax Rate']*100:.2f}%")
        st.markdown(f"**Specificities:** {country_info['Specificities']}")

    # Main Content
    col1, col2 = st.columns((2, 1))
    with col1:
        merged_data = gpd.GeoDataFrame(
            europe_geojson.merge(excel_data, left_on="name", right_on="Country")
        )
        merged_data["Tax Rate %"] = merged_data["Tax Rate"].apply(
            lambda x: f"{x*100:.2f}%"
        )

        linear = cm.LinearColormap(
            ["green", "yellow", "red"],
            vmin=excel_data["Tax Rate"].min(),
            vmax=excel_data["Tax Rate"].max(),
        )
        folium_map = folium.Map(location=[54.5260, 15.2551], zoom_start=4)
        tooltip = folium.features.GeoJsonTooltip(
            fields=["name", "Tax Rate %", "Specificities"],
            aliases=["Country", "Tax Rate", "Specificities"],
            sticky=False,
        )
        folium.GeoJson(
            data=merged_data,
            style_function=lambda feature: {
                "fillColor": linear(feature["properties"]["Tax Rate"]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            name="Tax Rate (%)",
            tooltip=tooltip,
        ).add_to(folium_map)
        folium_static(folium_map, width=1000, height=850)

    with col2:
        st.subheader("Methodological Notes")
        st.write(
            """
            This interactive map provides a visual representation of fiscal laws and tax rates for IT freelancers across Europe.
            Colors on the map indicate the relative tax rate, with green being the lowest and red the highest. Data is sourced from publicly available information and is updated regularly.
        """
        )
        # st.markdown(f"**Selected Country:** {selected_country}")
        # st.markdown(f"**Tax Rate:** {country_info['Tax Rate']*100:.2f}%")
        # st.markdown(f"**Specificities:** {country_info['Specificities']}")


if __name__ == "__main__":
    main()
