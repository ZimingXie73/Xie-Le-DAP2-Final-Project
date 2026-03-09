import streamlit as st
import pydeck as pdk
import json
import os

st.set_page_config(page_title="Environmental Regulation & Firm Dynamics Dashboard", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_BASE = os.path.join(BASE_DIR, "StreamlitGraph")
DATA_BASE = os.path.join(BASE_DIR, "StreamlitData")

@st.cache_data
def load_geojson(level):
    file_path = os.path.join(DATA_BASE, f"map_{level.lower()}.geojson")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_map(geojson_data, level):
    if not geojson_data:
        st.warning(f"Map data for {level} is missing.")
        return

    if level == "Province":
        tooltip_html = """
            <b>Prov Code:</b> {code}<br/>
            <b>Target Reduction:</b> {target_reduction}%<br/>
            <b>Actual Reduction:</b> {actual_reduction}%<br/>
            <b>Migration Rate:</b> {migration_rate}%<br/>
            <b>Enter Rate:</b> {enter_rate}%<br/>
            <b>Exit Rate:</b> {exit_rate}%
        """
    else:
        tooltip_html = """
            <b>Geo Code:</b> {code}<br/>
            <b>Actual Reduction:</b> {actual_reduction}%<br/>
            <b>Migration Rate:</b> {migration_rate}%<br/>
            <b>Enter Rate:</b> {enter_rate}%<br/>
            <b>Exit Rate:</b> {exit_rate}%
        """

    layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        pickable=True,
        stroked=True,
        filled=True,    
        extruded=False,
        get_fill_color=[30, 30, 30, 100], 
        get_line_color=[220, 220, 220, 255], 
        get_line_width=3000 if level == "Province" else (800 if level == "City" else 150),
    )

    view_state = pdk.ViewState(latitude=35.0, longitude=105.0, zoom=3.5, pitch=0)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"html": tooltip_html, "style": {"color": "white", "backgroundColor": "rgba(0,0,0,0.8)"}},
        map_style=pdk.map_styles.DARK
    )
    
    st.pydeck_chart(r, use_container_width=True, height=550)

st.sidebar.title("Navigation")
st.sidebar.markdown("Work of Ziming Xie & Le Sun: Explore spatial and micro-firm visualization.")

selected_level = st.sidebar.selectbox("Geographical Level:", ["Province", "City", "County", "Firm"])
selected_category = st.sidebar.radio("Analysis Category:", ["Emission Reduction", "Firm Dynamics"])

st.title(f"{selected_level} Level: {selected_category}")

if selected_level in ["Province", "City", "County"]:
    geo_data = load_geojson(selected_level)
    render_map(geo_data, selected_level)
    st.markdown("---") 


if selected_level == "Province":
    if selected_category == "Emission Reduction":
        st.image(os.path.join(IMG_BASE, "1.png"), use_container_width=True)
    elif selected_category == "Firm Dynamics":
        st.image(os.path.join(IMG_BASE, "2.png"), use_container_width=True)

elif selected_level == "City":
    if selected_category == "Emission Reduction":
        col1, col2 = st.columns(2)
        col1.image(os.path.join(IMG_BASE, "City-Level", "3.png"), use_container_width=True)
        col2.image(os.path.join(IMG_BASE, "City-Level", "4.png"), use_container_width=True)
    elif selected_category == "Firm Dynamics":
        r1_col1, r1_col2 = st.columns(2)
        r1_col1.image(os.path.join(IMG_BASE, "City-Level", "5.png"), use_container_width=True)
        r1_col2.image(os.path.join(IMG_BASE, "City-Level", "6.png"), use_container_width=True)
        st.image(os.path.join(IMG_BASE, "City-Level", "7.png"), width=800)

elif selected_level == "County":
    if selected_category == "Emission Reduction":
        st.image(os.path.join(IMG_BASE, "County-Level", "8.png"), use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.image(os.path.join(IMG_BASE, "County-Level", "9.png"), use_container_width=True)
        c2.image(os.path.join(IMG_BASE, "County-Level", "10.png"), use_container_width=True)
        c3.image(os.path.join(IMG_BASE, "County-Level", "11.png"), use_container_width=True)
    elif selected_category == "Firm Dynamics":
        pass

elif selected_level == "Firm":
    if selected_category == "Emission Reduction":
        st.image(os.path.join(IMG_BASE, "Firm-Level", "12.png"), use_container_width=True)
        st.markdown("---")
        c1, c2 = st.columns(2)
        c1.image(os.path.join(IMG_BASE, "Firm-Level", "14.png"), use_container_width=True)
        c2.image(os.path.join(IMG_BASE, "Firm-Level", "17.png"), use_container_width=True)
    elif selected_category == "Firm Dynamics":
        r1_c1, r1_c2 = st.columns(2)
        r1_c1.image(os.path.join(IMG_BASE, "Firm-Level", "13.png"), use_container_width=True)
        r1_c2.image(os.path.join(IMG_BASE, "Firm-Level", "14.png"), use_container_width=True)
        r2_c1, r2_c2 = st.columns(2)
        r2_c1.image(os.path.join(IMG_BASE, "Firm-Level", "15.png"), use_container_width=True)
        r2_c2.image(os.path.join(IMG_BASE, "Firm-Level", "16.png"), use_container_width=True)