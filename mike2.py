import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from openbb_terminal.core.plots.plotly_helper import OpenBBFigure, theme  # noqa: F401
from openbb_terminal.sdk import openbb

# Pull index data
data_indicies = openbb.economy.indices()
data_indicies[["Chg", "%Chg"]] = data_indicies[["Chg", "%Chg"]].apply(pd.to_numeric)
data_indicies = data_indicies.set_index(data_indicies.columns[0])



#Color outputs based positive
def color_negative_red(val):
    if type(val) != "str":
        color = "green" if val > 0 else "red"
        return f"color: {color}"
    
plot_onedf = openbb.economy.index(indices= ["dow_dji", "nasdaq", "sp500", "dow_djus", "russell2000", "nyse", "sp400", "cboe_vix"],
    interval = "1d",
    start_date = "2022-05-30",
    end_date = "2023-05-30",
    column = "Close",
    #returns: bool = False,
                    
)

#combining ym & es into the index dataframe
sp_futs = openbb.futures.historical(symbols = "ES", start_date = "2022-05-30", end_date = "2023-05-30")
sp_futs = sp_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])
dow_futs = openbb.futures.historical(symbols = "YM", start_date = "2022-05-30", end_date = "2023-05-30")
dow_futs = dow_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])

indicies_plot_df = pd.concat([plot_onedf, dow_futs, sp_futs], axis=1)
indicies_plot_df.columns = ["DJIA", "Nasdaq Composite", "S&P 500", "DJ Total Stock Market", "Russell 2000",
                            "NYSE Composite", "Barron's 400", "CBOE Volatility", "DJIA Futures", "S&P 500 Futures"
                           ]


#Streamlit

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    layout="wide",
    page_title="Bootcamp - Major Indicies Dashboard",
    page_icon="chart"
)
image_rut = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/rutgers2.png'
image_openbb = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/openbb_logo.png'
image_streamlit = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/streamlit_logo.png'


index_list = ["DJIA", "Nasdaq Composite", "S&P 500", "DJ Total Stock Market", "Russell 2000",
                "NYSE Composite", "Barron's 400", "CBOE Volatility", "DJIA Futures", "S&P 500 Futures"]

#header
col1, col2, col3, col4 = st.columns([50, 25, 25, 25])
with col1:
    st.image(image_rut, width = 250)
with col2:
    st.image(image_openbb, width = 300)
# with col3:
#     st.title("&")
with col4:
    st.image(image_streamlit, width = 300)


col1, col2 = st.columns([2.25, 4])
with col1:
    with st.container():
        st.subheader("Indicies Overview")
        data_indicies = openbb.economy.indices()
        data_indicies[["Chg", "%Chg"]] = data_indicies[["Chg", "%Chg"]].apply(pd.to_numeric)
        data_indicies = data_indicies.set_index(data_indicies.columns[0])
        st.dataframe(data_indicies.style.applymap(color_negative_red, subset=["Chg", "%Chg"]), use_container_width=True)
        st.subheader("Commodities")
        
with col2:
    with st.container():
        # st.subheader("Charts")
        # indicies = st.selectbox(label = "Choose an index", options = index_list)
        # title = st.write("Daily Close")
        selected_column = st.selectbox("Select Index", index_list)
        plt.plot(indicies_plot_df.index, indicies_plot_df[selected_column])
        st.pyplot()