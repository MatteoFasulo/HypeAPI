import streamlit as st
import pandas as pd

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

profile = load_profile()
profile = profile.iloc[0]

st.title(f"Welcome  {profile.firstname.capitalize()} {profile.lastname.capitalize()}!")
st.header("Account Information")
st.subheader("Phone Number")
st.write(profile.phone)
st.subheader("Email")
st.write(profile.email)
st.subheader("Address")
st.write(f"{profile.address}, {profile.city} ({profile.zipCode})")
st.divider()
st.header("Current Plan")
st.write(profile.userType)