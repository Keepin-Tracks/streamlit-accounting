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

grouped_df['Amount'] = grouped_df['Amount'].apply(lambda x: "${:.2f}".format(x))

# Display bar chart
st.bar_chart(grouped_df.set_index('Account'), )
