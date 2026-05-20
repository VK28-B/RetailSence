import streamlit as st
import pandas as pd
import plotly.express as px
from utils import calculate_revenue, classify_customer

st.set_page_config(page_title="RetailSense Dashboard", layout="wide")

@st.cache_data
def load_data():
    customers = pd.read_csv('data/customers.csv')
    orders = pd.read_csv('data/orders.csv')
    products = pd.read_csv('data/products.csv')
    
    full_df = orders.merge(customers, on='customer_id', how='left')
    full_df = full_df.merge(products, on='product_id', how='left')
    
    full_df['price'] = pd.to_numeric(full_df['price'], errors='coerce')
    full_df['quantity'] = pd.to_numeric(full_df['quantity'], errors='coerce')
    full_df['discount_pct'] = pd.to_numeric(full_df['discount_pct'], errors='coerce')
    full_df['rating'] = pd.to_numeric(full_df['rating'], errors='coerce')
    
    full_df['revenue'] = full_df.apply(
        lambda row: calculate_revenue(row['price'], row['quantity'], row['discount_pct']), 
        axis=1
    )
    full_df['age_group'] = full_df['age'].apply(classify_customer)
    
    return full_df

full_df = load_data()

st.title("🛒 RetailSense Analytics Dashboard")

with st.sidebar:
    st.header("Filters")
    selected_category = st.selectbox(
        "Select Category",
        ["All"] + sorted(full_df['category'].dropna().unique().tolist())
    )
    min_rating = st.slider("Minimum Product Rating", 1.0, 5.0, 1.0, 0.1)

filtered_df = full_df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

st.header("Overview Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_revenue = filtered_df['revenue'].sum()
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    total_orders = len(filtered_df)
    st.metric("Total Orders", total_orders)

with col3:
    avg_rating = filtered_df['rating'].mean()
    st.metric("Average Product Rating", f"{avg_rating:.2f}")

st.header("Data Table")
st.dataframe(filtered_df.head(50), width='stretch')

st.header("Analytics Charts")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    revenue_by_age = filtered_df.groupby('age_group')['revenue'].sum().reset_index()
    revenue_by_age = revenue_by_age.sort_values('revenue', ascending=False)
    fig_bar = px.bar(
        revenue_by_age,
        x='age_group',
        y='revenue',
        title='Revenue by Age Group',
        labels={'revenue': 'Revenue (₹)', 'age_group': 'Age Group'},
        color='revenue',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_bar, width='stretch')

with chart_col2:
    if len(filtered_df) > 0:
        fig_box = px.box(
            filtered_df,
            y='price',
            title=f'Price Distribution - {selected_category}',
            labels={'price': 'Price (₹)'}
        )
        st.plotly_chart(fig_box, width='stretch')

st.header("Upload & Inspect CSV")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)
    st.subheader("First 10 Rows")
    st.dataframe(df_upload.head(10), width='stretch')
    
    st.subheader("Data Statistics")
    st.dataframe(df_upload.describe(), width='stretch')