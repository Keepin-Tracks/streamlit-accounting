import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Transactions",
    ttl="10m",
)

# Add currency sign to 'Debit' column

# Group by 'Account' using Pandas.
grouped_df = df.groupby('Account')['Amount'].sum().reset_index()

grouped_df.style.format({'Amount': lambda val: f'${val:,.2f}'})
# Display bar chart
st.bar_chart(grouped_df.set_index('Account'), )
