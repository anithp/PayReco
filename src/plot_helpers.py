import streamlit as st

def display_metrics(metrics):
    # Extract only the first 10 metrics relevant to display_metrics
    total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees, gross_profit, net_profit, _, total_sales, *_ = metrics

    st.header('Key Metrics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Orders', total_orders)
    with col2:
        st.metric('Total Cancelled Orders', total_cancelled_orders)
    with col3:
        st.metric('Total Return Orders', total_return_orders)
    with col4:
        st.metric('Amazon Sharing Fees', f"₹{amazon_sharing_fees:,.2f}")

    col5, col6, col7, col8, col9 = st.columns(5)
    with col5:
        st.metric('Shipping Fees', f"₹{shipping_fees:,.2f}")
    with col6:
        st.metric('FBA Fees', f"₹{fba_fees:,.2f}")
    with col7:
        st.metric('Gross Profit', f"₹{gross_profit:,.2f}")
    with col8:
        st.metric('Net Profit', f"₹{net_profit:,.2f}")
    with col9:
        st.metric('Total Sales', f"₹{total_sales:,.2f}")

def display_critical_orders( mode_value, less_than_mode, greater_than_mode):
    st.header('Critical Orders from Reconciliation')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Normal Comission behaviour', mode_value)
    with col2:
        st.metric('Critical Commission number count', greater_than_mode)
    with col3:
        st.metric('Favourable Commission number count', less_than_mode)
    

def display_location_analysis(df):
    st.header('Location Analytics')
    location_counts = df['order city'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Order Count']
    st.dataframe(location_counts)

def display_sku_analysis(df):
    st.header('SKU Analytics')
    sku_counts = df['sku'].value_counts().reset_index()
    sku_counts.columns = ['SKU', 'Order Count']
    st.bar_chart(sku_counts.set_index('SKU'))
