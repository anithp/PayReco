import streamlit as st
import pandas as pd
from data_loader import load_data
from metrics_calculator import calculate_metrics, calculate_monthly_metrics, calculate_fulfillment_metrics
from plot_helpers import display_metrics, display_critical_orders, display_location_analysis, display_sku_analysis, display_monthly_metrics, display_fulfillment_comparison


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
        (total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees,
         gross_profit, net_profit, total_sales, mode_value, less_than_mode, greater_than_mode, df_greater_than_mode,
         loss_from_returned_orders) = metrics
        
        # Display Key Metrics
        display_metrics((total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees,
                         fba_fees, gross_profit, net_profit, total_sales))
        
        # Display Critical Orders and Related Metrics
        display_critical_orders(mode_value, less_than_mode, greater_than_mode, df_greater_than_mode)

        # Display Location Analysis
        display_location_analysis(df)

        # Display SKU Analysis
        display_sku_analysis(df)

        # Display Loss from Returned Orders
        st.header('Loss from Returned Orders')
        st.metric('Total Loss from Returned Orders', f"₹{loss_from_returned_orders:,.2f}")

        # Calculate and display Monthly Metrics

        monthly_metrics = calculate_monthly_metrics(df)
        display_monthly_metrics(monthly_metrics)

        # Calculate Comparision 

        fulfillment_metrics = calculate_fulfillment_metrics(df)
        display_fulfillment_comparison(fulfillment_metrics)

if __name__ == '__main__':
    main()
