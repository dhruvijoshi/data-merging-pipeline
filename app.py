import streamlit as st
import pandas as pd

st.title('Client Data Merging')
st.write('Merged Client Data')

client_df = pd.read_csv('data/clients_merged.csv')
# Merged data
st.dataframe(client_df) 

st.write(f'Number of unique clients: {len(client_df)}')

st.bar_chart(client_df['Source'].value_counts(), horizontal=True)