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
      padding-bottom: 0px;
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
        height: 100vh;
        overflow: hidden;
      }}
      [data-testid="stSidebarUserContent"] {{
        padding: 15px;
        max-height: calc(100vh - 72px - 25vh);
        overflow-y: scroll;
      }}
      [data-testid="stSidebarNavItems"] {{
        padding-top: 50px;
        height: 25vh;
        padding: 15px 0;
        display: flex;
        flex-direction: column;
        justify-content: end;
      }}
      [data-testid="stIFrame"] {{
        position: fixed;
        bottom: 10px;
        max-height: 60px;
        background: rgb(38, 39, 48);
        padding-top: 10px;
      }}
    </style>
  """,
    unsafe_allow_html=True)
