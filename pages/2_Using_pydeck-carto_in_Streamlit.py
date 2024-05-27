import streamlit as st
import streamlit.components.v1 as components
from pydeck_layers import deck_la
from common import set_page_container_style, set_sidebar_style

# Right Side

st.set_page_config(
    page_title="Wildfire Contribution Factors",
    page_icon="🔥",
    layout="wide",
)
set_page_container_style(padding_top=2, max_height=100)

st.markdown("Here you have the example code needed to create a map:")

code = '''
import pydeck as pdk
from carto_auth import CartoAuth
from pydeck_carto import get_layer_credentials
from pydeck_carto.layer import MapType
from pydeck_carto.styles import color_bins
import streamlit as st

# Authentication with CARTO
carto_auth = CartoAuth.from_oauth()

# Render CARTO layer in pydeck
listings_layer = pdk.Layer(
    "CartoLayer",
    data="SELECT * FROM  carto-demo-data.demo_tables.losangeles_airbnb_data",
    type_=MapType.QUERY,
    connection=pdk.types.String("carto_dw"),
    credentials=get_layer_credentials(carto_auth),
    get_fill_color=color_bins("price_num", [30, 100, 150, 300], "Sunset"),
    point_radius_min_pixels=2.5,
    opacity=0.4,
    pickable=True,
    stroked=False,
)

map_style = pdk.map_styles.CARTO_ROAD
view_state_la = pdk.ViewState(latitude=34, longitude=-118.4, zoom=9, pitch=20, bearing=30)
tooltip={"html": "Price: <b>{price_num}</b>", "style": {"color": "white"}}
la_listings = pdk.Deck(listings_layer, map_style=map_style, initial_view_state=view_state_la, tooltip=tooltip)

# Add the map to streamlit
st.pydeck_chart(la_listings)

'''
st.code(code, language='python')

st.pydeck_chart(deck_la)

# Left Side
generate_explanations = """
Pydeck-carto is a python library to render CARTO maps in jupyter notebooks and now in Streamlit. This integration allows 
the creation of interactive and scalable map visualizations directly within Python notebooks. 

This streamlined approach eliminates the need for context switching between different tools, allowing data scientists to 
iteratively explore their data and visualizations simultaneously within the notebook, and also sharing insights from 
their geospatial data thanks to Streamlit.

"""
st.sidebar.markdown(generate_explanations)

logos_component = open("logos_component.html", 'r', encoding='utf-8')
source_code = logos_component.read()
with st.sidebar.container():
    components.html(source_code)

set_sidebar_style()
