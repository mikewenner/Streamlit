import pandas as pd
import streamlit as st
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


sp_futs = openbb.futures.historical(symbols = "ES", start_date = "2022-05-30", end_date = "2023-05-30")
sp_futs = sp_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])
dow_futs = openbb.futures.historical(symbols = "YM", start_date = "2022-05-30", end_date = "2023-05-30")
dow_futs = dow_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])

indicies_plot_df = pd.concat([plot_onedf, dow_futs, sp_futs], axis=1)
indicies_plot_df.columns = ["DJIA", "Nasdaq Composite", "S&P 500", "DJ Total Stock Market", "Russell 2000",
                            "NYSE Composite", "Barron's 400", "CBOE Volatility", "DJIA Futures", "S&P 500 Futures"
                           
]

#djia = st.line_chart(indicies_plot_df["DJIA"])



#Streamlit
st.set_page_config(
    layout="wide",
    page_title="Bootcamp - Major Indicies Dashboard",
)

djia = st.line_chart(indicies_plot_df["DJIA"])
sp500 = st.line_chart(indicies_plot_df["S&P 500"])

#header
col1, col2, col3, col4 = st.columns([25, 25, 4, 25])
with col1:
    st.title("Market Data")
with col2:
    st.markdown("## RUTGERS BOOTCAMP")
with col3:
    st.markdown("## &")
with col4:
    st.markdown("## STREAMLIT")


col1, col2 = st.columns([2, 4])
with col1:
    with st.container():
        st.subheader("US Index Overview")
        data_indicies = openbb.economy.indices()
        data_indicies[["Chg", "%Chg"]] = data_indicies[["Chg", "%Chg"]].apply(pd.to_numeric)
        data_indicies = data_indicies.set_index(data_indicies.columns[0])
        st.dataframe(data_indicies.style.applymap(color_negative_red, subset=["Chg", "%Chg"]), use_container_width=True)
with col2:
    with st.container():
        st.subheader("Charts")
        st.selectbox(label = "Select", options = [djia, sp500])
