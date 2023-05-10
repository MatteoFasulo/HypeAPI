import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_movements():
    movements = pd.read_json('json/movements.json', orient='columns')
    month_movements = movements["month"]
    movements_data = [movement for month in month_movements for movement in month["movements"]]
    movements = pd.json_normalize(movements_data)
    return movements

st.set_page_config(layout='wide')
movements = load_movements()

left, right = st.columns(2)

with left:
    fig = px.bar(movements.groupby('subType').sum().reset_index().sort_values(by='amount',ascending=False), x='subType', y='amount', color='subType')
    # Add styling
    fig.update_layout(
        xaxis=dict(title='Transaction Type', tickangle=-45),
        yaxis=dict(title='Total Amount ($/EUR)'),
        plot_bgcolor='white',
        title=dict(text='Total amount per transaction type'),
        title_x=0.5,
        title_y=0.95,
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    subtype_count = movements.groupby(['subType', 'income']).size().reset_index(name='count')
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


movements = movements.sort_values('date')
movements['color'] = movements['income'].map({True: 'green', False: 'red'})

fig = px.scatter(movements, x='date', y='amount', size='amount', color='income',
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

# Display the scatter plot
st.plotly_chart(fig, use_container_width=True)
