# Explaining Wildfire Risk in California with GenAI
Demo project build with CARTO to show how wildfire risk can be explained with Snowflake Cortex

Avaliable here: https://carto-demo-wildfires.streamlit.app/

## How to run locally
### Prerequisites:
- Python 3.11+
- CARTO account
- Snowflake account with required data to visualize
- Connect CARTO account with Snowflake account using [this guide](https://docs.carto.com/carto-user-manual/connections/snowflake)

### Running locally
(Optional) Create a python container for this app

1. Navigate to project folder
2. Open `pydeck_layers.py` and replace `st.secrets["token"]` with your [CARTO API Token](https://docs.carto.com/carto-user-manual/developers/managing-credentials/api-access-tokens)
3. Run `pip install -r requirements.txt`
5. Run `streamlit run Explaining_Wildfire_Risk_in_California_with_GenAI.py`
6. App is available at http://localhost:8501
