import streamlit as st
import pandas as pd
from data_loader import load_data
from metrics_calculator import calculate_metrics
from plot_helpers import display_metrics, display_critical_orders, display_location_analysis, display_sku_analysis

def main():
    st.set_page_config(page_title="Ecommerce Analytics Dashboard", layout="wide")
    st.title('Ecommerce Analytics Dashboard')

    # File upload
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        
        st.write("Data Overview", df.head())

        # Calculate metrics
        metrics = calculate_metrics(df)
        display_metrics(metrics)
        
        # Display Critical Orders
        display_critical_orders(df)

        # Display Location Analysis
        display_location_analysis(df)

        # Display SKU Analysis
        display_sku_analysis(df)

if __name__ == '__main__':
    main()
