import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Transactions",
    ttl="10m",
)
df['Debit'] = df['Debit'].map(lambda x: f"${x:.00f}")

# Group by 'Account' using Pandas.
grouped_df = df.groupby('Account')['Debit'].sum().reset_index()

# Display bar chart
st.bar_chart(grouped_df.set_index('Account'))