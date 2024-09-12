from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import streamlit as st
import os
import pandas as pd
import plotly.express as px

class GoogleAnalyticsAPI:
    def __init__(self):
        self.property_id = os.environ.get('GA_PROPERTY_ID')
        self.client = BetaAnalyticsDataClient()

    def get_report(self, start_date, end_date, metrics, dimensions):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[{"start_date": start_date, "end_date": end_date}],
            metrics=[{"name": metric} for metric in metrics],
            dimensions=[{"name": dimension} for dimension in dimensions],
        )
        response = self.client.run_report(request)
        return response

def render_google_analytics_section():
    st.title("Google Analytics Integration")

    ga_api = GoogleAnalyticsAPI()

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Fetch Google Analytics Data"):
        metrics = ["totalUsers", "newUsers", "activeUsers", "sessions", "bounceRate"]
        dimensions = ["date"]

        try:
            response = ga_api.get_report(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), metrics, dimensions)
            
            data = []
            for row in response.rows:
                data.append({
                    "Date": row.dimension_values[0].value,
                    "Total Users": int(row.metric_values[0].value),
                    "New Users": int(row.metric_values[1].value),
                    "Active Users": int(row.metric_values[2].value),
                    "Sessions": int(row.metric_values[3].value),
                    "Bounce Rate": float(row.metric_values[4].value)
                })

            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['Date'])

            st.subheader("Google Analytics Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Users", df["Total Users"].sum())
            col2.metric("New Users", df["New Users"].sum())
            col3.metric("Active Users", df["Active Users"].sum())

            st.subheader("User Trends")
            fig = px.line(df, x="Date", y=["Total Users", "New Users", "Active Users"], title="User Trends Over Time")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Session and Bounce Rate")
            fig = px.scatter(df, x="Date", y="Sessions", size="Bounce Rate", title="Sessions and Bounce Rate Over Time")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching Google Analytics data: {str(e)}")

# Example usage:
# render_google_analytics_section()
