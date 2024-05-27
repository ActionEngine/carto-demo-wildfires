import streamlit as st
import streamlit.components.v1 as components
from pydeck_layers import (deck_fires,
                           deck_tavg, deck_tmax,
                           deck_wind, deck_prec,
                           deck_vp
                           )
from common import set_page_container_style, set_sidebar_style

# right side
st.set_page_config(
    page_title="Wildfire Contributing Factors",
    page_icon="🔥",
    layout="wide",
)
set_page_container_style(padding_top=1, max_height=100)
st.markdown("## Wildfire Contributing Factors")

# Tabs
tab_map, tab_factors = st.tabs(["California Wildfires", "Wildfire Contributing Factors"])
with tab_map:
    st.pydeck_chart(deck_fires)

    caption = """
    California wildfires. Source: Perimeters of different fires provided by Weather Source (historical data provided by 
    the Wildland Fire Management Research, Development  & Application group at the National Interagency Fire Center) 
    containing the start and end of each fire  cause of the ignition and burned area (BA).
    """
    st.caption(caption)
    wildfire_understanding = """
    Understanding wildfires better and evaluating wildfire risk can help save people, property and nature by developing 
    strategies aimed at wildfire prevention and mitigation. Not only that, but it would also be invaluable to business 
    owners and especially in insurance industry by allowing insurance policies and pricing to backed up by real wildfire 
    data analytics.
    """
    st.markdown(wildfire_understanding)
with tab_factors:
    caption_factor = """
    Source: Perimeters of different fires provided by Weather Source (historical data provided by the Wildland Fire 
    Management Research, Development & Application group at the National Interagency Fire Center) containing the start 
    and end of each fire cause of the ignition and burned area (BA).
    """
    tab_tmax, tab_tavg, tab_wind, tab_prec, tab_vp = st.tabs([
        "Maximum Temperature",
        "Average Temperature",
        "Wind Speed",
        "Precipitation",
        "Vapour Pressure"
    ])
    with tab_tmax:
        st.pydeck_chart(deck_tmax)
        st.caption(caption_factor)
    with tab_tavg:
        st.pydeck_chart(deck_tavg)
        st.caption(caption_factor)
    with tab_wind:
        st.pydeck_chart(deck_wind)
        st.caption(caption_factor)
    with tab_prec:
        st.pydeck_chart(deck_prec)
        st.caption(caption_factor)
    with tab_vp:
        st.pydeck_chart(deck_vp)
        st.caption(caption_factor)

# left side
wf_stats = """
To generate data explanations we will use data, which directly contributes to wildfire risk. Wildfires can occur for a 
number of reasons.\
In our case, we had data for California in the form of monthly average and maximum temperatures, average wind speed, average humidity, and average vapour pressure.
"""
st.sidebar.markdown(wf_stats)

logos_component = open("logos_component.html", 'r', encoding='utf-8')
source_code = logos_component.read()
with st.sidebar.container():
    components.html(source_code)

set_sidebar_style()
