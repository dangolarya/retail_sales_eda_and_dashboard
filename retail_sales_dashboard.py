import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

st.title("📊 Retail Sales Insight Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("Cleaned_retail_sales.csv")

df = load_data()
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

location_filter = st.sidebar.multiselect(
    "Select Location",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)

min_date = df['Transaction_Date'].min()
max_date = df['Transaction_Date'].max()

start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df[
    (df['Category'].isin(category_filter)) &
    (df['Location'].isin(location_filter)) &
    (df['Transaction_Date'] >= start_date) &
    (df['Transaction_Date'] <= end_date)
]

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['Total_sales'].sum()
    st.metric("Total_Revenue", f"${total_sales:,.2f}", border=True)

with col2:
    total_orders = filtered_df.shape[0]
    st.metric("Total Orders", total_orders, border=True)

with col3:
    avg_order = filtered_df['Total_sales'].mean()
    st.metric("Average Order Value", f"${avg_order:,.2f}", border=True)

with col4:
    top_category = filtered_df['Category'].mode()[0]
    st.metric("Top Category", top_category, border=True)

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("🛒 Sales by Product Category")

    sales_by_category = filtered_df.groupby('Category')['Total_sales'].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        x=sales_by_category.index,
        y=sales_by_category.values,
        ax=ax
    )

    plt.xticks(rotation=45)
    plt.ylabel("Revenue")

    st.pyplot(fig)

with right_col:
    st.subheader("💳 Payment Method Distribution")

    payment = filtered_df['Payment_Method'].value_counts()

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        payment,
        labels=payment.index,
        autopct='%1.1f%%',
        startangle=90
    )

    st.pyplot(fig)

st.subheader("📈 Monthly Sales Trend")

month_order = [
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ]

monthly_sales = filtered_df.groupby('Month')['Total_sales'].sum().reindex(month_order)

fig, ax = plt.subplots(figsize=(12,5))

sns.lineplot(
        x=monthly_sales.index,
        y=monthly_sales.values,
        marker='o',
        ax=ax
    )

plt.xticks(rotation=45)
plt.ylabel("Sales")

st.pyplot(fig)
left_2, right_2=st.columns(2)

with left_2:

    st.subheader("🔥 Correlation Heatmap")

    corr = filtered_df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax
    )

    st.pyplot(fig)
with right_2:
    st.subheader("🏆 Top Selling Products")
    cat=filtered_df['Category'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10,8))
    sns.barplot(y=cat.index, x=cat)
    plt.title('Top selling products')
    plt.xlabel('Number of products sold')
    st.pyplot(fig)

st.subheader("📄 Top 5 customers to contribute to total sales")
top_5_customers = (
    filtered_df[[
        'Customer_ID',
        'Category',
        'Total_sales',
        'Location',
    ]]
    .sort_values(
        by='Total_sales',
        ascending=False
    )
    .head(5)
)

st.dataframe(top_5_customers)
