import pandas as pd
import streamlit as st
# from openbb_terminal.core.plots.plotly_helper import OpenBBFigure, theme  # noqa: F401
from openbb_terminal.sdk import openbb

# pd.options.plotting.backend = "plotly"

data_indicies = openbb.economy.indices()
data_indicies[["Chg", "%Chg"]] = data_indicies[["Chg", "%Chg"]].apply(pd.to_numeric)
data_indicies = data_indicies.set_index(data_indicies.columns[0])

def highlight_max(cell):
    if type(cell) != str and cell < 0 :
        return 'background: red; color:black'
    else:
        return 'background: green; color: white'
  
data_indicies.style.applymap(highlight_max)

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

djia = indicies_plot_df.plot(y=["DJIA"], figsize = (10,10), title = "Dow Jones Industrial Average")
nasdaq = indicies_plot_df.plot(y=["Nasdaq Composite"], figsize = (10,10), title = "Nasdaq Composite Index")
sp500 = indicies_plot_df.plot(y=["S&P 500"], figsize = (10,10), title = "S&P 500")
total = indicies_plot_df.plot(y=["DJ Total Stock Market"], figsize = (10,10), title = "DJ Total Stock Market Index")
rut = indicies_plot_df.plot(y=["Russell 2000"], figsize = (10,10), title = "Russell 2000")
nyse = indicies_plot_df.plot(y=["NYSE Composite"], figsize = (10,10), title = "NYSE Composite")
baron = indicies_plot_df.plot(y=["Barron's 400"], figsize = (10,10), title = "Barrons 400")
vix = indicies_plot_df.plot(y=["CBOE Volatility"], figsize = (10,10), title = "VIX")
djifuts = indicies_plot_df.plot(y=["DJIA Futures"], figsize = (10,10), title = "DOW Futures")
spfuts = indicies_plot_df.plot(y=["S&P 500 Futures"], figsize = (10,10), title = "S&P Futures")

all = indicies_plot_df.plot(
    title = "All Indicies",
    figsize = (10,10), 
    #logy = True

)

st.set_page_config(
    layout="wide",
    page_title="Dashboard Powered by OpenBB & Streamlit",
)

col1, col2, col3, col4 = st.columns([25, 11, 4, 10])
with col1:
    st.title("Dashboard Powered By")
    st.write("Built by [Joseph B](https://twitter.com/DirtyDefi)")

with col2:
    st.image(
        "https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/images/openbb_logo.png",
        width=120,
    )

with col3:
    st.markdown(
        """

    # &
                """
    )

with col4:
    st.image(
        "https://raw.githubusercontent.com/mesmith027/streamlit-roboflow-demo/master/images/streamlit_logo.png",
        width=180,
    )