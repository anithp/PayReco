import streamlit as st
import pandas as pd

# Helper function to clean and convert columns to numeric
def clean_and_convert(df):
    # Strip whitespace and convert to lowercase for all column names
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Convert relevant columns to numeric, handling commas, whitespace, and non-numeric values
    numeric_cols = [
        'quantity', 'product sales', 'shipping credits', 'promotional rebates', 
        'total sales tax liable(gst before adjusting tcs)', 'tcs-cgst', 'tcs-sgst', 
        'tcs-igst', 'tds (section 194-o)', 'selling fees', 'fba fees', 
        'other transaction fees', 'other', 'total', 'estimated charges', 
        'margin on seller fees', 'charges on other transaction fees'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# Helper function to calculate metrics
def calculate_metrics(df):
    total_orders = total_return_orders = len(df[df['type'].str.contains('order', case=False, na=False)])-len(df[df['type'].str.contains('refund', case=False, na=False)])
    total_cancelled_orders = len(df[df['type'].str.contains('refund', case=False, na=False)])
    total_return_orders = len(df[df['type'].str.contains('refund', case=False, na=False)])
    amazon_sharing_fees = abs(df['selling fees'].sum())
    shipping_fees = abs(df['other transaction fees'].sum())
    fba_fees = abs(df['fba fees'].sum())
    total_sales = abs(df['product sales'].sum())
    gross_profit = df['total'].sum()
    net_profit = gross_profit - df['total sales tax liable(gst before adjusting tcs)'].sum() - df['tcs-cgst'].sum() - df['tcs-sgst'].sum() - df['tcs-igst'].sum() - df['tds (section 194-o)'].sum()
    critical_orders = df[df['type'].str.contains('critical', case=False, na=False)]
    return total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees, gross_profit, net_profit, critical_orders, total_sales

# Main Streamlit app
def main():
    st.set_page_config(page_title="Ecommerce Analytics Dashboard", layout="wide")
    st.title('Ecommerce Analytics Dashboard')

    # File upload
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Clean and convert column names
        df = clean_and_convert(df)
        
        st.write("Data Overview", df.head())

        # Calculate metrics
        metrics = calculate_metrics(df)
        total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees, gross_profit, net_profit, critical_orders, total_sales = metrics

        # Key Metrics Section
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

        # Critical Orders Section
        st.header('Critical Orders from Reconciliation')
        st.dataframe(critical_orders)

        # Location Analytics Section
        st.header('Location Analytics')
        location_counts = df['order city'].value_counts().reset_index()
        location_counts.columns = ['Location', 'Order Count']
        st.bar_chart(location_counts.set_index('Location'))

        # SKU Analytics Section
        st.header('SKU Analytics')
        sku_counts = df['sku'].value_counts().reset_index()
        sku_counts.columns = ['SKU', 'Order Count']
        st.bar_chart(sku_counts.set_index('SKU'))

if __name__ == '__main__':
    main()
