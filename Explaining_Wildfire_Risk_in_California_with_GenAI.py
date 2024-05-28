import sys
sys.path.append(".")

import streamlit as st
import streamlit.components.v1 as components
from pydeck_layers import deck_wri
from common import set_page_container_style, set_map_container_style, set_sidebar_style

st.set_page_config(
    page_title="Explaining Wildfire Risk in California with GenAI",
    page_icon="🔥",
    layout="wide",
)
set_page_container_style(padding_top=0, max_height=100)
set_map_container_style(max_map_height=55)

# Right Side
st.markdown("## Explaining Wildfire Risk in California with GenAI")

# Tabs
tab_app, tab_chart = st.tabs(["The App", "See LLM Prompt"])
with tab_app:
    st.text("Hover on an area in the map below to understand the wildfire risk")
    st.pydeck_chart(deck_wri)
with tab_chart:
    cortex_description = """
    To get this explanation, we will pass the calculated risk of wildfire along with it’s contribution factors 
    ([source](https://carto.com/blog/spatial-data-to-make-wildfire-risk-map)) for every H3 cell across California. 
    To achieve this, we create a new column in our Snowflake dataset, where we would store all the responses from the 
    Cortex COMPLETE function.
    """
    st.markdown(cortex_description)

    st.markdown("##### Snowflake Cortex Prompt below is used to create and write Cortex output to a new column:")

    code = '''SELECT *, SNOWFLAKE.CORTEX.COMPLETE(
    'mixtral-8x7b',
        CONCAT('Wildfire risk in certain place in August is ', WRI_KMEANS_5_CAT_JOINED, 
        '. Please explain it in a couple of sentences using the following information about this place: ', 
        'monthly average temperature is ', TAVG_AUG, ' Celsius, ',
        'monthly maximum temperature is ', TMAX_AUG, ' Celsius, ',
        'June precipitation is ', PREC_AUG, ' inches, ',
        'average wind speed is', WIND_AUG, 'm/s.',
        'average vapour pressure is', VAPR_AUG, 'Pa.',
        'Make your explanation as short as possible.'
        )
        '''
    st.code(code, language='sql')

    st.markdown("##### Example output from Cortex LLM from using the prompt above:")

    st.markdown('''
    >The wildfire risk in this place in August is high due to several factors.
    The average temperature isalready warm at 24.07 Celsius, but the monthly maximum of 32.27 Celsius can create even drier conditions.
    Additionally, the precipitation is very low at only 4.43 mm for the month, leaving the landscape parched. 
    The average wind speed of 2.9 m/s can help fan the flames of any fires that do start. Lastly, the average vapor pressure of 1.12 Pa indicates low atmospheric moisture, which can further exacerbate wildfire conditions.
    ''')

# Left Side

intro = '''
Many industries face not just potential, but very real risks from wildfires.The average total wildland fire 
[stats](https://www.fire.ca.gov/our-impact/statistics) in California show the occurrence of more than 1,200 wildfires 
affecting over 5,000 acres. Recent studies ([1](https://www.pnas.org/doi/10.1073/pnas.2011048118), 
[2](https://www.epa.gov/climate-indicators/climate-change-indicators-wildfires#:~:text=Multiple%20studies%20have%20found%20that%20wildfire%20frequency%2C%20and%20burned%20area.&text=The%20wildfire%20season%20has%20lengthened%20and%20drier%20soils%20and%20vegetation.)) 
confirm that wildfire risk is increasing in the United States, posing significant dangers to homeowners, farmers, and 
the forest industry. This issue is also a subject of study among insurance analysts, environmentalists, and sustainability 
professionals.<br><br> CARTO has a recent [study](https://carto.com/blog/spatial-data-to-make-wildfire-risk-map) aimed 
at gathering geospatial data to calculate wildfire risk groups across California where you can see risk in every H3 cell 
across California rated from Low to Very High. In this exercise <span style='text-decoration:underline'>we want to go deeper into the explainability of this 
model so that a wider audience</span> (i.e homeowners or insurance policy makers) can really understand what’s behind this. 
Here, [**Snowflake Cortex LLM**](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions) can help 
explain why an area has been labeled with a particular risk category. 
'''
st.sidebar.markdown(intro, unsafe_allow_html=True)

logos_component = open("logos_component.html", 'r', encoding='utf-8')
source_code = logos_component.read()
with st.sidebar.container():
    components.html(source_code)

set_sidebar_style()
