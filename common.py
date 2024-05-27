import streamlit as st


def set_page_container_style(padding_top=0, max_height=0, overflow="unset"):
    st.markdown(
        f'''
  <style>
    .block-container {{
      padding-top: {padding_top}rem;
      max-height: {max_height}% !important;
      overflow: {overflow};
    }}
    h2 {{
      padding-bottom: 0;
    }}
  </style>
  ''',
        unsafe_allow_html=True,
    )


def set_map_container_style(max_map_height=0):
  st.markdown(
    f'''
  <style>
    #deckgl-wrapper {{
      max-height: {max_map_height}vh;
    }}
  </style>
  ''',
    unsafe_allow_html=True,
)


def set_sidebar_style():
  st.markdown(
    f"""
    <style>
    [data-testid="stSidebarContent"] {{
      max-height: 100vh !important;
      overflow: hidden;
    }}
    [data-testid="stSidebarUserContent"] {{
      padding: 15px;
    }}
    [data-testid="stSidebarNavItems"] {{
      padding-top: 50px;
    }}
    [data-testid="stSidebarUserContent"] > div:nth-child(1) {{
      max-height: 63vh;
      overflow-y: scroll;
    }}
    [data-testid="stIFrame"] {{
      position: fixed;
      bottom: 10px;
      max-height: 100px;
      padding-top: 10px;
      background: rgb(38, 39, 48);
    }}
    </style>
  """,
    unsafe_allow_html=True)
