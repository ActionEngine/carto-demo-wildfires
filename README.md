#  ❤️‍🔥 Explaining Wildfire Risk in California with GenAI

This repository contains the source code for [Explaining Wildfire Risk in California with GenAI](https://carto-demo-wildfires.streamlit.app/)

![Screenshot 2024-07-18 160418](https://github.com/user-attachments/assets/1543f08e-ae73-4f02-a80e-fb0fd20c37ee)

## 💻 How to run locally
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
6. App will be available at http://localhost:8501

## 💬 Contact us
Reach out to us at info@actionengine.com
