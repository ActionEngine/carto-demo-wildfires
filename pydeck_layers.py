import pydeck as pdk
from pydeck_carto.styles import color_bins
from carto_auth import CartoAuth
from pydeck_carto import get_layer_credentials
from pydeck_carto.layer import MapType, GeoColumnType
from pydeck.types import Image

# Carto authentication and vars
carto_auth = CartoAuth.from_oauth(cache_filepath='./token_oauth.json')
# map_style = pdk.map_styles.LIGHT
map_style = "https://actionengine-public.s3.us-east-2.amazonaws.com/carto_demo/carto_road_style.json"
view_state = pdk.ViewState(latitude=37.4, longitude=-121.5, zoom=9, pitch=0, bearing=0)

# Fires
fires_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT GEOM, ROUND(GIS_ACRES, 2) AS GIS_ACRES, FIRE_NAME FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.OTHER_WILDFIRES_2020 WHERE YEAR=2020""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_polygon="GEOM",
    spatial_data_column="GEOM",
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    # get_fill_color=color_bins("TAVG_AUG", [22, 23, 24, 25], "Peach"),
    get_fill_color=[255, 20, 0, 150],
    get_line_color=[102, 51, 0, 100],
    line_width_min_pixels=2,
)

tooltip_fires = {
    "html":
        "<b>Fire Name:</b> <br>{FIRE_NAME}<br><b>Fire Area (Acres):</b> <br>{GIS_ACRES}",
    "style":
        {"color": "white"}
}

view_state_california = pdk.ViewState(latitude=37.4, longitude=-121.5, zoom=5, pitch=0, bearing=0)
deck_fires = pdk.Deck(fires_layer, map_style=map_style, initial_view_state=view_state_california, tooltip=tooltip_fires)

# WRI
wri_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, CAST(SUBSTRING(WRI_KMEANS_5_CAT_JOINED, 1, 1) as int) AS WRI_CODE, WRI_KMEANS_5_CAT_JOINED, EXPLANATION FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("WRI_CODE", [4, 5], "BurgYl"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("""AVG(WRI_CODE) as WRI_CODE, 
                                     MODE(WRI_KMEANS_5_CAT_JOINED) as WRI_KMEANS_5_CAT_JOINED,
                                     MODE(EXPLANATION) as EXPLANATION"""),
    aggregation_res_level=8,
)

tooltip_wri = {
    "html":
        """<b>Wildfire Risk Index:</b> <br>{WRI_KMEANS_5_CAT_JOINED}<br>
        <b>Explanation:</b> <br>{EXPLANATION}""",
    "style":
        {"color": "white"}
}
deck_wri = pdk.Deck(wri_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_wri)

# Temperature
tavg_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(TAVG_AUG, 1) AS TAVG_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("TAVG_AUG", [22, 23, 24, 25], "Peach"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("AVG(TAVG_AUG) as TAVG_AUG"),
    aggregation_res_level=8,
)

tooltip_tavg = {
    "html":
        "<b>Average August Temperature (Celsius):</b> <br>{TAVG_AUG}",
    "style":
        {"color": "white"}
}

tmax_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(TMAX_AUG, 1) AS TMAX_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("TMAX_AUG", [29, 30, 31, 32], "Peach"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("AVG(TMAX_AUG) as TMAX_AUG"),
    aggregation_res_level=8,
)

tooltip_tmax = {
    "html":
        "<b>Maximum August Temperature (Celsius):</b> <br>{TMAX_AUG}",
    "style":
        {"color": "white"}
}

deck_tavg = pdk.Deck(tavg_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_tavg)
deck_tmax = pdk.Deck(tmax_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_tmax)

# Wind
wind_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(WIND_AUG, 2) AS WIND_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("WIND_AUG", [2, 3, 4], "Mint"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("AVG(WIND_AUG) as WIND_AUG"),
    aggregation_res_level=8,
)

tooltip_w = {
    "html":
        "<b>Average August Wind Speed (m/s):</b> <br>{WIND_AUG}",
    "style":
        {"color": "white"}
}
deck_wind = pdk.Deck(wind_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_w)

# Precipitation
prec_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(PREC_AUG, 2) AS PREC_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("PREC_AUG", [3, 4, 5, 6], "BluYl"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("AVG(PREC_AUG) as PREC_AUG"),
    aggregation_res_level=8,
)

tooltip_p = {
    "html":
        "<b>Average August Precipitation (inches):</b> <br>{PREC_AUG}",
    "style":
        {"color": "white"}
}
deck_prec = pdk.Deck(prec_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_p)

# Vapour Pressure
vp_layer = pdk.Layer(
    "CartoLayer",
    data="""SELECT H3, ROUND(VAPR_AUG, 2) AS VAPR_AUG FROM PARTNER_ACTION_ENGINE_DB.WILDFIRE.PIECE_1000_EXPLANATION_AUGUST""",
    type_=MapType.QUERY,
    connection=pdk.types.String("sf_partner_conn"),
    credentials=get_layer_credentials(carto_auth),
    geo_column=GeoColumnType.H3,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    hexagonAggregator=False,
    get_fill_color=color_bins("VAPR_AUG", [0.5, 1, 1.5], "BluYl"),
    get_line_color=[103, 8, 8, 100],
    line_width_min_pixels=2,
    aggregation_exp=pdk.types.String("AVG(VAPR_AUG) as VAPR_AUG"),
    aggregation_res_level=8,
)

tooltip_vp = {
    "html":
        "<b>Average August Vapour Pressure (Pa):</b> <br>{VAPR_AUG}",
    "style":
        {"color": "white"}
}
deck_vp = pdk.Deck(vp_layer, map_style=map_style, initial_view_state=view_state, tooltip=tooltip_vp)
