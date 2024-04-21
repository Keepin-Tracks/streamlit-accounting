import streamlit as st
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Transactions",
    ttl="10m",
)
df.dropna(inplace=True)

df['all'] = 'all'

df['Abs_Amount'] = df['Amount'].abs()


fig = px.treemap(df,
                 path=['all', 'Account', 'Date'],
                 values='Abs_Amount',
                 color='Amount',
                 color_continuous_scale='RdBu',
                 color_continuous_midpoint=0)

st.write("Keepin'Tracks Accounting")

st.plotly_chart(fig, use_container_width=True)

st.link_button("Plotly's Treemap Documentation", "https://plotly.com/python/treemaps/")
st.link_button("Streamlit's Link Button", "https://docs.streamlit.io/develop/api-reference/widgets/st.link_button")
# Add currency sign to 'Debit' column

# # Group by 'Account' using Pandas.
# grouped_df = df.groupby('Account')['Amount'].sum().reset_index()

# grouped_df['Amount'] = grouped_df['Amount'].apply(lambda x: "${:.2f}".format(x))

# # Display bar chart
# st.bar_chart(grouped_df.set_index('Account'), )
