# Explaining Wildfire Risk in California with GenAI
Demo project build with CARTO to show how wildfire risk can be explained with Snowflake Cortex

Avaliable here: https://carto-demo-wildfires.streamlit.app/

## How to run locally
### Prerequisites:
- Python 3.11+
- Carto account
- Snowflake account with needed data to visualize
- Carto account connection with Snowflake account

### Running
1. run oAuth.py and login into Carto in browser (this will create a token_oauth.json file)
2. pip install requirements.txt
3. streamlit run app.py
4. open localhost:8501
