import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

@st.cache_data
def load_balance():
    balance = pd.read_json('json/balance.json', orient='index').transpose()
    return balance

@st.cache_data
def load_card():
    card = pd.read_json('json/card.json', orient='index').transpose()
    card_settings = pd.json_normalize(card['setting'][0]['operations'])
    return card, card_settings

@st.cache_data
def load_movements():
    movements = pd.read_json('json/movements.json', orient='columns')
    month_movements = movements["month"]
    movements_data = [movement for month in month_movements for movement in month["movements"]]
    movements = pd.json_normalize(movements_data)
    return movements

@st.cache_data
def load_profile():
    profile = pd.read_json('json/profile.json', orient='index').transpose()
    return profile


st.write('Profile')
st.dataframe(load_profile())

st.write('Balance')
st.dataframe(load_balance())

st.write('Card')
card, card_settings = load_card()
st.dataframe(card)

st.write('Card Settings')
st.dataframe(card_settings)

st.write('Movements')
st.dataframe(load_movements())