import streamlit as st
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Transactions",
    ttl="10m", # Time before refetching data
)
df.dropna(inplace=True)

@st.cache_data(ttl=3600)
def get_categories():
    df = conn.read(
        worksheet="Categories",
        ttl="10m",
    )
    df.dropna(inplace=True)
    return df

@st.cache_data(ttl=3600)
def get_subGroups():
    df = conn.read(
        worksheet="SubGroups",
        ttl="10m",
    )
    df.dropna(inplace=True)
    return df

@st.cache_data(ttl=3600)
def get_accounts():
    df = conn.read(
        worksheet="Accounts",
        ttl="10m",
    )
    df.dropna(inplace=True)
    return df

df_categories = get_categories()
df_subGroups = get_subGroups()
df_accounts = get_accounts()

df['all'] = 'all'

# df.join(df_categories)
df = df.join(df_accounts.set_index('Account'), on='Account')
df['Abs_Amount'] = df['Amount'].abs()


fig = px.treemap(df,
                 path=['all','SubGroup', 'Account', 'Date'],
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
