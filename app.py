import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
from app_db import sectors
from app_db import macros

col1, col2 = st.beta_columns(2)


# @st.cache
def load_data(stock_list, start_date):
    data_list = [yf.download(stock, start_date)['Close'] for stock in stock_list]
    data = pd.concat(data_list, axis=1)
    data.columns = [code for code in stock_list]
    # long_name = [yf.Ticker(ticker).info['longName'] for ticker in data.columns]

    return data


# sidebar construct
st.sidebar.title('Stocks to Watch')
start_date = st.sidebar.date_input("주가그래프 시작일을 선택하세요. 디폴트 2020/1/1", value=date(2020, 1, 1))
sector_choice = st.sidebar.selectbox('섹터를 선택하세요', [k for k in sectors.keys()])
stock_list = st.sidebar.multiselect('Select Stocks', sectors[sector_choice], sectors[sector_choice])
st.sidebar.write('----------------------')
st.sidebar.title('Macro Indicator')
st.sidebar.write('WORKS TO DO')
macro_choice = st.sidebar.selectbox('인디케이터 선택하세요', [k for k in macros.keys()])
macro_list = st.sidebar.multiselect('Select Indicators', macros[macro_choice], macros[macro_choice])
st.sidebar.text('copyright by Taeyoon Lee')


df = load_data(sectors[sector_choice], start_date)

n = 1
for stock in stock_list:
    day0_price = df[stock][-1]
    day1_price = df[stock][-2]
    note_up = f'price: {round(day0_price,2)} up by {(day0_price/day1_price -1)*100:.2f} %'
    note_down = f'price: {round(day0_price, 2)}  down by {(day0_price / day1_price - 1) * 100:.2f} %'
    if n == 1:
        col1.title(stock)
        # col1.write(company_name[count])
        if day0_price >= day1_price:
            col1.write(note_up)
        else:
            col1.write(note_down)
        col1.line_chart(df[stock])
        n = 2
    elif n == 2:
        col2.title(stock)
        # col2.write(company_name[count])
        if day0_price >= day1_price:
            col2.write(note_up)
        else:
            col2.write(note_down)
        col2.line_chart(df[stock])
        n = 1


