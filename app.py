import streamlit as st
from pydeck_layers import (deck_fires, deck_wri,
                        deck_tavg, deck_tmax,
                        deck_wind, deck_prec,
                        deck_vp, chart_data)


st.set_page_config(page_title="Using Snowflake Cortex to explain Fire Risk Index")
st.header("Using Snowflake Cortex to explain Fire Risk Index", divider="rainbow")

# ------ Intro ------

st.subheader("Snowflake Cortex in geospatial analysis")
intro = '''
Geospatial analysis of data is not a simple task not only to data analysis but also to those who need to see and 
understand the results of analysis, but are not knowledgeable in data analysis or data science. With tools like 
Snowflake Cortex, Carto and Streamlit it is made easy to generate presentable data analysis results to wider audiences.
'''
st.markdown(intro)
st.markdown('##### What is Snowflake Cortex?')
cortex_description = """
Snowflake Cortex is a service that offers machine learning and AI solutions to Snowflake users, which includes:\n
- LLM Functions: SQL and Python functions that leverage large language models (LLMs) for understanding, querying, 
translating, summarizing, and generating free-form text.\n
- Machine Learning Functions: SQL functions that perform predictive analysis using machine learning to help you gain 
insights into your structured data and accelerate everyday analytics.\n
Available fully in Snowflake, Cortex can directly provide insights on top of existing analytical tools in Snowflake, 
which allows enhancing data analysis.\n
One of the LLM functions is the [COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex) function. It performs complex reasoning with data, just like you would expect 
from GPT LLM’s. For example, a great usage of this function would be data explanation, which would make the presentation 
of data much more comprehensible to whoever you are presenting it: be it a data analyst, marketing team or your aunt.\n
To demonstrate it on a real example, let’s take a look at how data on Wildfire Risk in California can be explained in 
a simple tooltip:
"""
st.markdown(cortex_description)
st.pydeck_chart(deck_wri)
st.caption('**Wildfire Risk Index** with explanation added by **Cortex COMPLETE** function')

about_tooltip = """
This tooltip has been made by Snowflake Cortex and then passed onto Carto’s Visualization for quick and easy 
representation within this Streamlit.\n
How did we do it? Let’s follow the story below.

"""
st.markdown(about_tooltip)

st.divider()

# ------ Problem Description, Fires Map ------
st.subheader("Use Case: Wildfire Risk in California")
wf_stats = """
Many industries can suffer not potential, but very real risks from wildfires. Average California total wildland fire 
[stats](https://www.fire.ca.gov/our-impact/statistics) shows the occurrence of more than 1,200 wildfires affecting more 
than 5,000 acres. Recent studies ([1](https://www.pnas.org/doi/10.1073/pnas.2011048118), 
[2](https://www.epa.gov/climate-indicators/climate-change-indicators-wildfires#:~:text=Multiple%20studies%20have%20found%20that%20wildfire%20frequency%2C%20and%20burned%20area.&text=The%20wildfire%20season%20has%20lengthened%20and%20drier%20soils%20and%20vegetation.)) confirm, 
that in the United States, wildfires risk is growing, and it can be specifically dangerous to house owners, farmers, 
forest industry and is a subject of study among insurance analysts, environmentalists and sustainability professionals.
"""
st.markdown(wf_stats)

st.markdown("##### California Wildfires Map")
st.pydeck_chart(deck_fires)
st.caption("Source")

st.markdown("##### Total Acres Burned by Year")
st.bar_chart(chart_data, x="YEAR_", y="GIS_ACRES")
st.caption("Source")

wf_understanding = '''
Understanding wildfires better and evaluating wildfire risk can help save people, property and nature by developing 
strategies aimed at wildfire prevention and mitigation. Not only that, but it would also be invaluable to business 
owners and especially in insurance industry by allowing insurance policies and pricing to backed up by real wildfire 
data analytics.\n
Carto has a recent [study](https://carto.com/blog/spatial-data-to-make-wildfire-risk-map) aimed at gathering geospatial 
data to calculate wildfire risk groups across California, however presenting these groups without context is not 
convincing to a wider audience. Here, Snowflake Cortex can help explain the data.
'''

st.markdown(wf_understanding)
st.divider()

# ------ Secondary Data ------
st.subheader("Wildfires contribution factors")
generate_explanations = """
To generate data explanations we will use data, which directly contributes to wildfire risk. Wildfires can occur for a 
number of reasons. In our case, we had data for California in the form of monthly average and maximum temperatures, 
average wind speed, average humidity, and average vapour pressure.
"""
st.markdown(generate_explanations)
st.markdown("##### Average and Maximum August Temperature")

# Tabs
tab_avg, tab_max = st.tabs(["Average", "Maximum"])
with tab_avg:
    st.pydeck_chart(deck_tavg)
    st.caption("Source")
with tab_max:
    st.pydeck_chart(deck_tmax)
    st.caption("Source")

# Render average August wind CartoLayer in pydeck:
st.markdown("##### Average August Wind Speed")
st.pydeck_chart(deck_wind)

st.markdown("##### Average August Precipitation")
st.pydeck_chart(deck_prec)
st.caption("Source")

# Render average August Vapour Pressure CartoLayer in pydeck:
st.markdown("##### Average August Vapour Pressure")
st.pydeck_chart(deck_vp)
st.caption("Source")
st.divider()

# ------ Cortex  ------
st.subheader("Data preparation and Snowflake Cortex COMPLETE function use.")
cortex = """To make Cortex work, we will pass to it the wildfire risk groups data along with the wildfire contribution 
factors [source](https://carto.com/blog/spatial-data-to-make-wildfire-risk-map), but that would not be enough as we would want to later visualize the outputs of Cortex on a map for 
every H3 cell across California. To achieve this, we should create a new column in our Snowflake dataset, where we would 
store all the responses from Cortex COMPLETE function.
"""
st.markdown(cortex)
st.markdown("##### Snowflake Cortex Prompt below is used to create and write Cortex output to a new column:")

code = '''SELECT *, SNOWFLAKE.CORTEX.COMPLETE(
    'mixtral-8x7b',
        CONCAT('Wildfire risk in certain place in June is ', WRI_KMEANS_5_CAT_JOINED, 
        '. Please explain it in a couple of sentences using the following information about this place: ', 
        'monthly average temperature is ', TAVG_AUG, ' Celsius, ',
        'monthly maximum temperature is ', TMAX_AUG, ' Celsius, ',
        'June precipitation is ', PREC_AUG, ' inches, ',
        'average wind speed is', WIND_AUG, 'm/s.',
        'average vapour pressure is', VAPR_AUG, 'Pa.',
        'Make your explanation as short as possible.'
        )'''
st.code(code, language='sql')


st.markdown("##### Example output from Cortex LLM from using the prompt above:")

st.markdown('''
>The wildfire risk in this place in June is high due to several factors.
The average temperature isalready warm at 24.07 Celsius, but the monthly maximum of 32.27 Celsius can create even drier conditions.
Additionally, the precipitation is very low at only 4.43 mm for the month, leaving the landscape parched. 
The average wind speed of 2.9 m/s can help fan the flames of any fires that do start. Lastly, the average vapor pressure of 1.12 Pa indicates low atmospheric moisture, which can further exacerbate wildfire conditions.
''')
st.divider()


# ------ Cortex Results on a map ------
st.subheader("Visualizing results made easy")
visualizing = """
Now that we have all the data we need along with the explanation for our data, we’d want to visualize it to present it. 
One of the easiest and fastest way to do that is via a Carto map visualizations (using 
[pydeck-carto](https://pydeck-carto.readthedocs.io/en/latest)) on a Streamlit app.
"""
st.markdown(visualizing)

st.pydeck_chart(deck_wri)
st.caption('**Wildfire Risk Index** with explanation added by **Cortex COMPLETE** function.')

st.divider()
integration = """
The world of geospatial data analytics is vast and complex, but using Streamlit’s pydeck and pydeck-carto integration 
you can easily show data accessed through Carto on a Snowflake-Carto connection with a blazing-fast response time and 
easy interactivity.
"""
st.markdown(integration)
st.image('https://actionengine-public.s3.us-east-2.amazonaws.com/carto_demo/logos.svg')
st.divider()
st.markdown("Brought to you by")
st.image("https://actionengine-public.s3.us-east-2.amazonaws.com/carto_demo/AE.svg", width=200)
