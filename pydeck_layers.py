import pydeck as pdk
from pydeck_carto.styles import color_bins
from carto_auth import CartoAuth
from pydeck_carto import get_layer_credentials
from pydeck_carto.layer import MapType, GeoColumnType
from pydeck.types import Image
from snowflake.snowpark.session import Session
import streamlit as st

carto_auth = CartoAuth(
    mode="oauth",
    api_base_url="https://gcp-us-east1.api.carto.com",
    access_token=st.secrets["token"],
    expiration=4155310800,
    open_browser=False
)

map_style = pdk.map_styles.CARTO_ROAD
view_state = pdk.ViewState(latitude=37.352, longitude=-121.575, zoom=8, pitch=0, bearing=0)
view_state_california = pdk.ViewState(latitude=37.4, longitude=-121.5, zoom=5, pitch=0, bearing=0)

tooltip_style = {
                 "color": "white",
                 "backgroundColor": "#1A212D",
                 "border-radius": "4px",
                 "padding": "1em",
                 "opacity": "1",
                 "z-index": "999999",
                }
tooltip_wri_style = tooltip_style.copy()
tooltip_wri_style["padding"] = "10px"
tooltip_wri_style["transform"] = "translate(0%, 56vh)"
tooltip_wri_style["line-height"] = "1em"
tooltip_wri_style["max-width"] = "100%"
tooltip_wri_style["font-size"] = "15px"

# Fires
fires_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT GEOM, ROUND(GIS_ACRES, 2) AS ACRES, FIRE_NAME, YEAR FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.OTHER_WILDFIRES_2020""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_polygon="GEOM",
    spatial_data_column="GEOM",
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=[255, 20, 0, 100],
    get_line_color=[102, 51, 0, 150],
    line_width_min_pixels=2,
)

tooltip_fires = {
    "html":
        "Fire Name: <br><b>{FIRE_NAME}</b><br>Fire Area (Acres): <br><b>{ACRES}</b><br>Year: <br><b>{YEAR}</b>",
    "style":
        tooltip_style
}
deck_fires = pdk.Deck(fires_layer, map_style=map_style, initial_view_state=view_state_california, tooltip=tooltip_fires)

# Fires histogram
# Snowflake authentication
SF_ACCOUNT = 'sxa81489.us-east-1'
SF_USER = 'PARTNER_ACTIONENGINE'
SF_PASSWORD = 'Yesterday123!'

connection_parameters = {
    "account": SF_ACCOUNT,
    "user": SF_USER,
    "password": SF_PASSWORD,
    "database": "PARTNER_ACTION_ENGINE_DB",
    "schema": "WILDFIRE",
    "warehouse": "PARTNER_ACTION_ENGINE_WH"
}

session = Session.builder.configs(connection_parameters).create()
q = 'SELECT YEAR_ AS YEAR, SUM(GIS_ACRES) AS ACRES FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.OTHER_WILDFIRES_2020 GROUP BY YEAR_ ORDER BY YEAR_'

chart_data = session.sql(q).to_pandas()

# WRI
wri_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, CAST(SUBSTRING(REPLACE(WRI_KMEANS_5_CAT_JOINED, 'No risk', '0 No risk'), 1, 1) as int) AS WRI_CODE, WRI_KMEANS_5_CAT_JOINED, EXPLANATION FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE TAVG_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("WRI_CODE", [1, 2, 3, 4, 5], "OrYel"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("""ROUND(AVG(WRI_CODE), 2) as WRI_CODE, 
                                     MODE(WRI_KMEANS_5_CAT_JOINED) as WRI_KMEANS_5_CAT_JOINED,
                                     MODE(EXPLANATION) as EXPLANATION"""),
    # aggregation_res_level=8,
    # min_zoom=6
)

tooltip_wri = {
    "html":
        """<span style="color: salmon; font-weight: bold; font-size: 16px;">Wildfire Risk Index:</span> <br>{WRI_KMEANS_5_CAT_JOINED}<br>
        <span style="color: salmon; font-weight: bold; opacity: 0.7;">Explanation:</span> <br>{EXPLANATION}""",
    "style":
        tooltip_wri_style
}
deck_wri = pdk.Deck(wri_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_wri)

# Temperature

tavg_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(TAVG_AUG, 2) AS TAVG_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE TAVG_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("TAVG_AUG", [22, 23, 24, 25], "Peach"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("ROUND(AVG(TAVG_AUG), 2) as TAVG_AUG"),
    # aggregation_res_level=8,
)

tooltip_tavg = {
    "html":
        "Average August Temperature (Celsius): <br><b>{TAVG_AUG}</b>",
    "style":
        tooltip_style
}

tmax_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(TMAX_AUG, 2) AS TMAX_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE TMAX_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("TMAX_AUG", [29, 30, 31, 32], "Peach"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("ROUND(AVG(TMAX_AUG), 2) as TMAX_AUG"),
    # aggregation_res_level=8,
)

tooltip_tmax = {
    "html":
        "Maximum August Temperature (Celsius): <br><b>{TMAX_AUG}</b>",
    "style":
        tooltip_style
}

deck_tavg = pdk.Deck(tavg_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_tavg)
deck_tmax = pdk.Deck(tmax_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_tmax)

# Wind
wind_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(WIND_AUG, 2) AS WIND_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE WIND_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("WIND_AUG", [2, 3, 4], "Mint"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("ROUND(AVG(WIND_AUG), 2) as WIND_AUG"),
    # aggregation_res_level=8,
)

tooltip_w = {
    "html":
        "Average August Wind Speed (m/s): <br><b>{WIND_AUG}</b>",
    "style":
        tooltip_style
}
deck_wind = pdk.Deck(wind_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_w)

# Precipitation
prec_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(PREC_AUG, 2) AS PREC_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE PREC_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("PREC_AUG", [3, 4, 5, 6], "BluYl"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("ROUND(AVG(PREC_AUG), 2) as PREC_AUG"),
    # aggregation_res_level=8,
)

tooltip_p = {
    "html":
        "Average August Precipitation (inches): <br><b>{PREC_AUG}</b>",
    "style":
        tooltip_style
}
deck_prec = pdk.Deck(prec_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_p)

# Vapour Pressure
vp_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(VAPR_AUG, 2) AS VAPR_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.WRI_EXPLANATION_FULL WHERE VAPR_AUG IS NOT NULL""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    auto_highlight=True,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("VAPR_AUG", [0.5, 1, 1.5], "BluYl"),
    opacity=0.2,
    get_line_color=[255, 255, 255, 150],
    line_width_min_pixels=1,
    aggregation_exp=pdk.types.String("ROUND(AVG(VAPR_AUG), 2) as VAPR_AUG"),
)

tooltip_vp = {
    "html":
        "Average August Vapour Pressure (Pa): <br><b>{VAPR_AUG}</b>",
    "style":
        tooltip_style
}
deck_vp = pdk.Deck(vp_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_vp)

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

view_state_la = pdk.ViewState(latitude=34, longitude=-118.4, zoom=9, pitch=20, bearing=30)
tooltip = {"html": "Price: <b>{price_num}</b>", "style": {"color": "white"}}
deck_la = pdk.Deck(listings_layer, map_style=map_style, initial_view_state=view_state_la, tooltip=tooltip)
