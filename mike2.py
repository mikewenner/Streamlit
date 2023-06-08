import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openbb_terminal.core.plots.plotly_helper import OpenBBFigure, theme  # noqa: F401
from openbb_terminal.sdk import openbb

# Pull index data
data_indicies = openbb.economy.indices()
data_indicies[["Chg", "%Chg"]] = data_indicies[["Chg", "%Chg"]].apply(pd.to_numeric)
data_indicies = data_indicies.set_index(data_indicies.columns[0])

#Pull commodity data
data_commodities = openbb.economy.futures()
data_commodities[["Chg", "%Chg"]] = data_commodities[["Chg", "%Chg"]].apply(pd.to_numeric)
data_commodities = data_commodities.set_index(data_commodities.columns[0])

#Color outputs based positive
def color_negative_red(val):
    if type(val) != "str":
        color = "green" if val > 0 else "red"
        return f"color: {color}"
    
start = (date.today() - relativedelta(months=12)).strftime('%Y-%m-%d')
end = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

#Create df for plotting    
plot_onedf = openbb.economy.index(indices= ["dow_dji", "nasdaq", "sp500", "dow_djus", "russell2000", "nyse", "sp400", "cboe_vix"],
    interval = "1d",
    start_date = start,
    end_date = end,
    column = "Close",
    #returns: bool = False,
)

#combining ym & es into the index dataframe, they are not incorporated in economy.index pull
sp_futs = openbb.futures.historical(symbols = "ES", start_date = start, end_date = end)
sp_futs = sp_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])
dow_futs = openbb.futures.historical(symbols = "YM", start_date = start, end_date = end)
dow_futs = dow_futs.drop(columns=["Open", "High", "Low", "Adj Close", "Volume"])

#create commodities df for plotting
symbols = ["cl", "bz", "gc", "si", "ng", "rb", "hg", "zc", "zw"]
comm_df = openbb.futures.historical(symbols = symbols, start_date = start, end_date = end)
comm_df = comm_df.iloc[:,0:9]
comm_df.columns = ["Brent Crude","Crude Oil","Gold","Copper","Natural Gas","Unleaded Gasoline","Silver","Corn","Wheat"]

#Final df for plotting Indicies & commodities
indicies_plot_df = pd.concat([plot_onedf, dow_futs, sp_futs, comm_df], axis=1)
indicies_plot_df.columns = ["DJIA", "Nasdaq Composite", "S&P 500", "DJ Total Stock Market", "Russell 2000",
                            "NYSE Composite", "Barron's 400", "CBOE Volatility", "DJIA Futures", "S&P 500 Futures",
                           "Brent Crude","Crude Oil","Gold","Copper","Natural Gas","Unleaded Gasoline","Silver","Corn","Wheat"
                           
                           ]


#Streamlit

st.set_option('deprecation.showPyplotGlobalUse', False)  #this needed to remove warning when st.pyplot() called

st.set_page_config(
    layout="wide",
    page_title="Bootcamp - Major Indicies Dashboard",
    page_icon="chart"
)
image_rut = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/rutgers2.png'
image_openbb = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/openbb_logo.png'
image_streamlit = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/streamlit_logo.png'


index_list = ["DJIA", "Nasdaq Composite", "S&P 500", "DJ Total Stock Market", "Russell 2000",
                "NYSE Composite", "Barron's 400", "CBOE Volatility", "DJIA Futures", "S&P 500 Futures",
                "Brent Crude","Crude Oil","Gold","Copper","Natural Gas","Unleaded Gasoline","Silver","Corn","Wheat"
                ]

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
        data_commodities = openbb.economy.futures()
        data_commodities[["Chg", "%Chg"]] = data_commodities[["Chg", "%Chg"]].apply(pd.to_numeric)
        data_commodities = data_commodities.set_index(data_commodities.columns[0])
        data_commodities = data_commodities.drop(data_commodities.index[-1])
        st.dataframe(data_commodities.style.applymap(color_negative_red, subset=["Chg", "%Chg"]), use_container_width=True)
        
with col2:
    with st.container():
        selected_column = st.selectbox("Select Index", index_list)
        plt.plot(indicies_plot_df.index, indicies_plot_df[selected_column])
        st.pyplot()

col1, col2, col3 = st.columns([2.5, 5, 1])
with col2:
        st.subheader("Calendar of Economic Events")
        data = openbb.economy.events()
        data = data.set_index(data.columns[0])
        st.dataframe(data)

st.subheader("Enter Your Favorite Stock Symbol")

text_input = st.text_input("Symbol").upper()
new_data = openbb.stocks.load(text_input)
new_data