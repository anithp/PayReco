def calculate_metrics(df):
    total_orders = len(df[df['type'].str.contains('order', case=False, na=False)])
    total_cancelled_orders = len(df[df['type'].str.contains('refund|cancelled', case=False, na=False)])
    total_return_orders = len(df[df['type'].str.contains('refund', case=False, na=False)])
    amazon_sharing_fees = abs(df['selling fees'].sum())
    shipping_fees = abs(df['other transaction fees'].sum())
    fba_fees = abs(df['fba fees'].sum())
    total_sales = abs(df['product sales'].sum())
    gross_profit = total_sales - amazon_sharing_fees - shipping_fees - fba_fees
    net_profit = gross_profit - df['total sales tax liable(gst before adjusting tcs)'].sum() - df['tcs-cgst'].sum() - df['tcs-sgst'].sum() - df['tcs-igst'].sum() - df['tds (section 194-o)'].sum()
    critical_orders = df[df['type'].str.contains('critical', case=False, na=False)]
    return total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees, gross_profit, net_profit, critical_orders, total_sales
