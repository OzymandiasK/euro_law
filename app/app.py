import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import branca.colormap as cm
import os


def main():
    st.title("European Freelancer Fiscal Laws Map")

    # Sidebar for selecting a country and displaying specific information
    st.sidebar.header("Country Details")
    # Load the Excel data into a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "Fiscal_data_EU.xlsx")
    excel_data = pd.read_excel(data_path)
    excel_data["Tax Rate"] = pd.to_numeric(excel_data["Tax Rate"], errors="coerce")

    # Dropdown for selecting a country
    country_list = excel_data["Country"].unique().tolist()
    selected_country = st.sidebar.selectbox("Select a country:", country_list)

    # Display selected country tax details
    country_info = excel_data[excel_data["Country"] == selected_country]
    if not country_info.empty:
        st.sidebar.markdown(
            f"**Tax Rate:** {country_info['Tax Rate'].values[0]*100:.2f}%"
        )
        st.sidebar.markdown(
            f"**Specificities:** {country_info['Specificities'].values[0]}"
        )
    else:
        st.sidebar.write("No data available for the selected country.")

    # Ensure the GeoJSON file is read into a GeoDataFrame
    geojson_path = os.path.join(current_dir, "europe.geojson")
    europe_geojson = gpd.read_file(geojson_path)

    # Merge and format data
    merged_data = gpd.GeoDataFrame(
        europe_geojson.merge(excel_data, left_on="name", right_on="Country")
    )
    merged_data["Tax Rate %"] = merged_data["Tax Rate"].apply(lambda x: f"{x*100:.2f}%")

    linear = cm.LinearColormap(
        ["green", "yellow", "red"],
        vmin=excel_data["Tax Rate"].min(),
        vmax=excel_data["Tax Rate"].max(),
    )

    # Map creation
    folium_map = folium.Map(location=[54.5260, 15.2551], zoom_start=4)
    tooltip = folium.features.GeoJsonTooltip(
        fields=["name", "Tax Rate %", "Specificities"],
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

    folium.GeoJson(
        data=merged_data,
        style_function=style_function,
        name="Tax Rate (%)",
        tooltip=tooltip,
    ).add_to(folium_map)
    folium_static(folium_map, width=1250, height=900)

    # Display source links as clickable URLs in an expander to reduce clutter
    with st.expander("Source Links"):
        for _, row in excel_data.iterrows():
            st.markdown(f"[{row['Country']}]({row['Source']})", unsafe_allow_html=True)

    # Methodological Notes Expander
    with st.expander("Methodological Notes"):
        st.write(
            """
            This interactive map is designed to provide an overview of freelancer fiscal laws and tax rates across Europe. 
            The colors on the map indicate the relative tax rate, with green being the lowest and red the highest. 
            The data is sourced from publicly available information and is regularly updated to reflect the latest rates and laws.
            For specific inquiries or detailed analysis, consulting a tax professional is recommended.
        """
        )


if __name__ == "__main__":
    main()
