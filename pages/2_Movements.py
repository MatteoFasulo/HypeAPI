import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

@st.cache_data
def load_balance():
    balance = pd.read_json('json/balance.json', orient='index').transpose()
    balance = balance.iloc[0]
    return balance

@st.cache_data
def load_movements():
    movements = pd.read_json('json/movements.json', orient='columns')
    month_movements = movements["month"]
    movements_data = [movement for month in month_movements for movement in month["movements"]]
    movements = pd.json_normalize(movements_data)
    movements = movements.sort_values('date')
    movements.date = pd.to_datetime(movements.date, utc=False, format='%Y-%m-%dT%H:%M:%SZ').dt.date
    movements['month'] = pd.to_datetime(movements.date).dt.month
    movements['month_name'] = pd.to_datetime(movements.date).dt.month_name()
    movements['year'] = pd.to_datetime(movements.date).dt.year
    return movements

st.set_page_config(layout='wide')

movements = load_movements()
balance = load_balance()
filtered_movements = movements.copy()

with st.sidebar:
    st.sidebar.title('Hype Account Dashboard')
    movement_types = movements.subType.unique().tolist()
    movement_types.insert(0, 'All')
    transaction_type = st.selectbox('Transaction Type', options=movement_types, index=movement_types.index('All'), help='None (Imposta di Bollo)')
    date_range = st.date_input('Date Range', value=[movements.date.min(), movements.date.max()], min_value=movements.date.min(), max_value=movements.date.max(), help='Date range of transactions')
    if transaction_type != 'All':
        filtered_movements = filtered_movements[filtered_movements['subType'] == transaction_type]
    try:
        filtered_movements = filtered_movements[(filtered_movements['date'] >= date_range[0]) & (filtered_movements['date'] <= date_range[1])]
    except IndexError:
        pass
    
st.title('Hype Bank Account Dashboard')
st.subheader('Summary')
left, midleft, midright, right = st.columns(4)
with left:
    st.metric('Total Balance', balance.balance)
with midleft:
    st.metric('Spendable', balance.spendable)
with midright:
    st.metric('Scheduled Activities', balance.scheduledActivities)
with right:
    st.metric('Saved for Goals', balance.savedAmountForGoals)

st.subheader('Transactions')
st.dataframe(filtered_movements)

st.subheader('Charts')

# barchart
fig = px.bar(filtered_movements.groupby('subType').sum().reset_index().sort_values(by='amount',ascending=False), x='subType', y='amount', color='subType')
fig.update_layout(
    xaxis=dict(title='Transaction Type', tickangle=-45),
    yaxis=dict(title='Total Amount ($/EUR)'),
    plot_bgcolor='white',
    title=dict(text='Total amount per transaction type'),
    title_x=0.5,
    title_y=0.95,
)
st.plotly_chart(fig, use_container_width=True)

# sunburst
subtype_count = filtered_movements.groupby(['subType', 'income']).size().reset_index(name='count')
subtype_count['label'] = subtype_count['income'].map({True: 'In', False: 'Out'})
fig = px.sunburst(subtype_count, path=['subType', 'label'], values='count',
                color='subType',
                hover_data=['count'])
fig.update_layout(
title=dict(text='Movements SubType Sunburst Chart'), 
title_x=0.5,
title_y=0.95,
)
st.plotly_chart(fig, use_container_width=True)

# scatterplot
filtered_movements['color'] = filtered_movements['income'].map({True: 'green', False: 'red'})
fig = px.scatter(filtered_movements, x='date', y='amount', size='amount', color='income',
                 hover_data=['title', 'subType', 'amount', 'date', 'additionalInfo.category.name'],
                 color_discrete_map={True: 'green', False: 'red'})
fig.update_layout(
    xaxis=dict(title='Date'),
    yaxis=dict(title='Amount ($/EUR)'),
    plot_bgcolor='white',
    title=dict(text='Bank Transactions Scatter Plot', font=dict(size=24)),
    title_x=0.25,
    title_y=0.95,
)
st.plotly_chart(fig, use_container_width=True)

# 
grouped_df = filtered_movements.groupby(['year', 'month', 'month_name', 'income'])['amount'].sum().reset_index()
grouped_df['month_year'] = grouped_df['month_name'] + ' ' + grouped_df['year'].astype(str)
color_map = {True: 'green', False: 'red'}


st.write(grouped_df)

fig = px.bar(grouped_df, x='month_year', y='amount', color='income',
             barmode='group', labels={'income': 'Income'}, title='Monthly Income', color_discrete_map=color_map)
fig.update_layout(
    legend=dict(itemclick='toggle'),
    clickmode='event+select'
)
st.plotly_chart(fig, use_container_width=True)