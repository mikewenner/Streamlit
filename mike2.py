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

#Create df's for plotting    
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
image_rut_bootcamp = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/rutgers.png'
image_openbb = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/openbb_logo.png'
image_streamlit = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/streamlit_logo.png'
#image_money = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/money.png'
#image_exchange = 'https://raw.githubusercontent.com/mikewenner/Streamlit/main/Images/exchange.png'



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

st.markdown("\n\n\n\n")
st.markdown("\n\n\n\n")

# Dashboard DataFrames & corresponding plots
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
        plt.xticks(rotation=30)
        st.pyplot()

st.markdown("\n\n\n\n")

# Economic event calendar
col1, col2, col3 = st.columns([2.5, 5, 1])
with col2:
    st.subheader("Calendar of Economic Events")
    data = openbb.economy.events()
    data = data.set_index(data.columns[0])
    st.dataframe(data)

st.markdown("\n\n\n\n")

# Single stock interaction
st.subheader("Enter Your Favorite Stock Symbol")

text_input = st.text_input("Symbol").upper()

# Company overview, balance sheet & earnings surprise dataframes & csv download
col1, col2, col3 = st.columns([3, 6, 6])
with col1:
    st.subheader("Company Overview")
    overview = openbb.stocks.fa.overview(text_input)
    overview
    if st.button("Company Overview CSV"):
        file_name = f"exported_data_{text_input}_Company Overview.csv"
        st.download_button(label="Download CSV", data=overview.to_csv(index=True), file_name=file_name)
with col2:
    st.subheader("Company Balance Sheet") # need list of column headers to pass in
    bal_sheet = openbb.stocks.fa.balance(text_input)
    bal_sheet
    if st.button("Balance Sheet CSV"):
        file_name = f"exported_data_{text_input}_Balance Sheet.csv"
        st.download_button(label="Download CSV", data=bal_sheet.to_csv(index=True), file_name=file_name)
with col3:
    st.subheader("Earnings Surprise") # **need to handle the "-" strings before can apply the coloring**
    earnings = openbb.stocks.fa.earnings(text_input)
    earnings
    if st.button("Earnings Surprise CSV"):
        file_name = f"exported_data_{text_input}_Earnings Surprise.csv"
        st.download_button(label="Download CSV", data=earnings.to_csv(index=False), file_name=file_name)

st.markdown("\n\n\n\n")
st.markdown("\n\n\n\n")

#Single stock plots price, price tgts & dividend
col1, col2 = st.columns([4, 4])
with col1:
    with st.container():
        st.subheader(f"Historical 5yr Price:  {text_input}")
        new_data = openbb.stocks.fa.historical_5(text_input)
        new_data = new_data["Close"]
        plt.plot(new_data, color="green")
        plt.xticks(rotation=30)
        plt.ylabel('Price ($)', labelpad=15)  # Adjust labelpad to position the label
        plt.gca().yaxis.set_label_coords(1.15, 0.5)
        plt.legend(loc = "upper left")
        st.pyplot()
with col2:
    with st.container():
        st.subheader(f"Analyst Price Target:  {text_input}")
        pt = openbb.stocks.fa.pt(text_input)
        pt = pt.drop(columns = ["Company", "Rating"])
        plt.plot(pt)
        plt.xticks(rotation=30)
        plt.ylabel('Price Target ($)', labelpad=15)  # Adjust labelpad to position the label
        plt.gca().yaxis.set_label_coords(1.15, 0.5)
        plt.legend(loc = "upper left")
        st.pyplot()

col1, col2 = st.columns([4, 4])
with col1:
    with st.container():
        st.subheader(f"Company Dividend Overview:  {text_input}")
        divs = openbb.stocks.fa.divs(text_input)
        for column in divs.columns:
            plt.plot(divs[column], label=column)
        plt.xticks(rotation=30)
        plt.ylabel('Qtr Div ($/Share)', labelpad=15)  # Adjust labelpad to position the label
        plt.gca().yaxis.set_label_coords(1.15, 0.5)
        plt.legend(loc = "upper center")
        st.pyplot()
with col2:
    with st.container():
        st.subheader(f"Dividend Closer Look:  {text_input}")
        divs = openbb.stocks.fa.divs(text_input)
        for column in divs.columns:
            plt.plot(divs[column], label=column)
        plt.xticks(rotation=30)
        plt.ylabel('Qtr Div (log scale)', labelpad=15)
        plt.yscale("log")
        plt.gca().yaxis.set_label_coords(1.15, 0.5)
        plt.legend(loc = "upper center")
        st.pyplot()   

st.markdown("\n\n\n\n")
st.markdown("\n\n\n\n")

#Bottom image and thanks
col1, col2, col3 = st.columns([2.25, 5, 1])
with col2:
    st.image(image_rut_bootcamp, width = 750)

st.markdown("\n\n\n\n")
st.markdown("\n\n\n\n")

col1, col2, col3 = st.columns([2.25, 5, 1])
with col2:
    st.write("Many thanks to my project team in this Bootcamp:  Eli, Omar & Ron - You guys are awesome!!")
    st.write("Thanks Dave & Hassan for a great Bootcamp & an incredible experience!!!")