import streamlit as st
import pandas as pd
import plotly.express as px
from marketing_channels import get_marketing_channel_data
from kpi_visualization import get_kpi_data
from woocommerce_integration import get_woocommerce_data
from task_management import get_tasks

def render_dashboard():
    st.title("E-commerce Marketing Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Marketing Channel Overview")
        channel_data = get_marketing_channel_data()
        fig = px.bar(channel_data, x="Channel", y="Progress", title="Marketing Channel Progress")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Key Performance Indicators")
        kpi_data = get_kpi_data()
        fig = px.line(kpi_data, x="Date", y=["CTR", "Conversion Rate", "Engagement"], title="KPI Trends")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("WooCommerce Insights")
        woo_data = get_woocommerce_data()
        fig = px.pie(woo_data, values="Revenue", names="Product", title="Revenue by Product")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Upcoming Tasks")
        tasks = get_tasks()
        st.table(tasks[["Task", "Due Date", "Status"]])

    st.markdown("---")
    st.write("Welcome to your personalized e-commerce marketing dashboard. Here you can view an overview of your marketing efforts, key performance indicators, WooCommerce insights, and upcoming tasks.")
