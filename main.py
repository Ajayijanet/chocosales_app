import streamlit as st
import pandas as pd
# altair plotting library
import altair as alt

def load_data():
    df = pd.read_csv("Chocosales.csv")
    # convert Date col to datetime datatype
    df.Date= pd.to_datetime(df.Date, format="%d-%b-%y")
    # convert the Amount col to float datatype
    df.Amount= df.Amount.str.replace("$","").str.replace(",","").str.strip().astype("float")
    df["Price/Box"] = round(df.Amount / df["Boxes Shipped"],2)


    return df

df = load_data()


# App Title
st.title("Chocolate Sales App")

# create filters
filters = {
    "Sales Person": df["Sales Person"].unique(),
    "Country": df["Country"].unique(),
    "Product":  df["Product"],
}

# store user selection
selected_filters = {}

# generate multi-select widget manually
for key, options in filters.items():
    selected_filters[key]=st.sidebar.multiselect(key,options)

    # lets have the full data
    filtered_df = df.copy()

    # apply filter selection to the data
    for key, selected_values in selected_filters.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[key].isin(selected_values)]


# display the data
st.dataframe(df.head())

# calculations
no_of_transactions = len(filtered_df)
total_revenue = filtered_df["Amount"].sum()
total_boxes = filtered_df["Boxes Shipped"].sum()
no_of_products = filtered_df["Product"].nunique()

# streamlit column component
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Transactions", no_of_transactions)
with col2:
    st.metric("Total Revenue", total_revenue)
with col3:
    st.metric("Total boxes", total_boxes)
with col4:
    st.metric("Product",no_of_products)
# charts
st.subheader("Products with largest revenue")

top_products= filtered_df.groupby("Product")["Amount"].sum().nlargest(5).reset_index()

st.write(top_products)

st.subheader("Top 5 Producrs by Revenue")
# configure the bar chrt
chart1 = alt.Chart(top_products).mark_bar().encode(
     x=alt.X('Amount:Q', title="Revenue ($)"),
     y=alt.Y("Product:N"),
    color=alt.Color("Product:N",legend=None)
 ).properties(height=300)

# display the chart
st.altair_chart(chart1, use_container_width=True)

# Chart2
st.subheader("Countries with the highest revenue")
Sales_by_Country = filtered_df.groupby("Country")["Amount"].sum().nlargest(8).reset_index()
st.write(Sales_by_Country)

st.subheader("Sales by country")
# Creating a pie chart
chart2 = alt.Chart(Sales_by_Country).mark_arc().encode(
    theta=alt.Theta('Amount:Q'),
    color=alt.Color("Country:N"),
    tooltip=["Country", 'Amount']
).properties(height=300, width=300,
             title="Sales by 6 different countries"
)
# display the pie chart
st.altair_chart(chart2, use_container_width=True)



# Chart3
st.subheader("Sales person with largest revenue")
Sales_Persons = filtered_df.groupby("Sales Person")["Amount"].sum().nlargest(10).reset_index()
st.write(Sales_Persons)

st.subheader("Top 10 Sales person by revenue")
# Create the bar chart
chart3 = alt.Chart(Sales_Persons).mark_bar().encode(
    y=alt.Y('Amount:Q', title="Revenue ($)"),
    x=alt.X("Sales person:N"),
    color=alt.Color("Sales Person:N",legend=None)
).properties(height=600)

# display the chart
st.altair_chart(chart3, use_container_width=True)


# Monthly Sales Trend
import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    df = pd.read_csv("Chocosales.csv")
    # convert Date col to datatime
    df.Date = pd.to_datetime(df.Date, format="%d-%b-%y").sort_values()
    df.Month = df.Date.dt.strftime('%b')
    # convert Amount col to float datatype
    df.Amount= df.Amount.str.replace("$","").str.replace(",","").str.strip().astype("float")
    return df
df = load_data()

st.subheader("Monthly Sales Trend")
Monthly_Sales = filtered_df.groupby(df.Month)['Amount'].sum().reset_index()
st.write(Monthly_Sales)

# creating a line graph between Months and Revenue
chart4 = alt.Chart(Monthly_Sales).mark_line(point=True).encode(
    x=alt.X('Date', title="Months"),
    y=alt.Y('Amount', title="Revenue ($)")
).properties(
    width=400,
    height=500,
    title='Monthly Sales Revenue'
)

# show line chart
st.altair_chart(chart4, use_container_width=True)
