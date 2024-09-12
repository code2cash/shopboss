import streamlit as st
import pandas as pd
import plotly.express as px
from woocommerce import API
import logging

logging.basicConfig(level=logging.INFO)

def connect_store():
    st.subheader("Connect Your WooCommerce Store")
    wordpress_url = st.text_input("WordPress URL (e.g., https://example.com)", key="woo_wordpress_url")
    consumer_key = st.text_input("Consumer Key", key="woo_consumer_key")
    consumer_secret = st.text_input("Consumer Secret", key="woo_consumer_secret")
    
    if st.button("Test Connection", key="woo_test_connection"):
        if wordpress_url and consumer_key and consumer_secret:
            try:
                wcapi = API(
                    url=wordpress_url,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    version="wc/v3"
                )
                response = wcapi.get("products")
                if response.status_code == 200:
                    st.success("Connection successful!")
                    st.session_state.woo_credentials = {
                        "url": wordpress_url,
                        "consumer_key": consumer_key,
                        "consumer_secret": consumer_secret
                    }
                else:
                    st.error("Connection failed. Please check your credentials.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in all fields.")

def get_woocommerce_data():
    if "woo_credentials" in st.session_state:
        wcapi = API(
            url=st.session_state.woo_credentials["url"],
            consumer_key=st.session_state.woo_credentials["consumer_key"],
            consumer_secret=st.session_state.woo_credentials["consumer_secret"],
            version="wc/v3"
        )
        products = wcapi.get("products").json()
        orders = wcapi.get("orders").json()
        
        # Process the data and return a DataFrame
        data = []
        for product in products:
            revenue = sum([float(order["total"]) for order in orders if order["line_items"] and order["line_items"][0]["product_id"] == product["id"]])
            order_count = len([order for order in orders if order["line_items"] and order["line_items"][0]["product_id"] == product["id"]])
            data.append({
                "Product": product["name"],
                "Revenue": revenue,
                "Orders": order_count
            })
        return pd.DataFrame(data)
    else:
        # Return mock data if no credentials are available
        return pd.DataFrame({
            "Product": ["Product A", "Product B", "Product C", "Product D"],
            "Revenue": [5000, 3000, 2000, 1000],
            "Orders": [100, 75, 50, 25]
        })

def render_woocommerce_insights():
    st.title("WooCommerce Insights")
    
    connect_store()
    
    if "woo_credentials" in st.session_state:
        st.success("Using real WooCommerce data")
    else:
        st.warning("Using mock data. Connect your store to see real data.")
    
    woo_data = get_woocommerce_data()

    # Revenue by product
    st.subheader("Revenue by Product")
    fig = px.pie(woo_data, values="Revenue", names="Product", title="Revenue Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Orders by product
    st.subheader("Orders by Product")
    fig = px.bar(woo_data, x="Product", y="Orders", title="Number of Orders")
    st.plotly_chart(fig, use_container_width=True)

    # Total revenue and orders
    total_revenue = woo_data["Revenue"].sum()
    total_orders = woo_data["Orders"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Orders", total_orders)

    # Top selling products
    st.subheader("Top Selling Products")
    top_products = woo_data.sort_values("Orders", ascending=False).head(3)
    st.table(top_products)

    # Add some explanatory text
    st.markdown("""
    This dashboard provides key insights from your WooCommerce store:
    - **Revenue by Product**: Shows how much each product contributes to your total revenue.
    - **Orders by Product**: Displays the number of orders for each product.
    - **Total Revenue and Orders**: Gives you a quick overview of your store's performance.
    - **Top Selling Products**: Lists your best-performing products by number of orders.

    Use these insights to make informed decisions about your product lineup, pricing, and marketing strategies.
    """)
