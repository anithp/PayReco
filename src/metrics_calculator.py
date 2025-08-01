import pandas as pd
import numpy as np

def calculate_metrics(df):
    total_orders = len(df[df['type'].str.contains('order', case=False, na=False)]) - len(df[df['type'].str.contains('refund|cancelled', case=False, na=False)])
    total_cancelled_orders = len(df[df['type'].str.contains('refund|cancelled', case=False, na=False)])
    total_return_orders = len(df[df['type'].str.contains('refund', case=False, na=False)])
    amazon_sharing_fees = abs(df['selling fees'].sum())
    shipping_fees = abs(df['other transaction fees'].sum())
    fba_fees = abs(df['fba fees'].sum())
    
    # Calculate total sales for rows where type contains 'order'
    total_sales = abs(df[df['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(df[df['type'].str.contains('refund', case=False, na=False)]['product sales'].sum())
    
    gross_profit = total_sales - amazon_sharing_fees - shipping_fees - fba_fees
    net_profit = gross_profit - df['total sales tax liable(gst before adjusting tcs)'].sum() - df['tcs-cgst'].sum() - df['tcs-sgst'].sum() - df['tcs-igst'].sum() - df['tds (section 194-o)'].sum()
    
    # Calculate mode and counts for 'estimated_selling_commission'
    if 'estimated_selling_commission' in df.columns and not df['estimated_selling_commission'].isna().all():
        mode_value = df['estimated_selling_commission'].mode().values[0] if not df['estimated_selling_commission'].mode().empty else np.nan
        if pd.notna(mode_value):
            less_than_mode = len(df[df['estimated_selling_commission'] < mode_value])
            greater_than_mode = len(df[df['estimated_selling_commission'] > mode_value])
            df_greater_than_mode = df[df['estimated_selling_commission'] > mode_value]
        else:
            less_than_mode = greater_than_mode = 0
            df_greater_than_mode = pd.DataFrame()  # Empty DataFrame if no valid mode
    else:
        mode_value = np.nan
        less_than_mode = greater_than_mode = 0
        df_greater_than_mode = pd.DataFrame()  # Empty DataFrame if no valid mode

    # Calculate loss from returned orders
    returned_orders = df[df['type'].str.contains('refund', case=False, na=False)]['order id'].unique()
    print(returned_orders)
    shipping_orders = df[df['type'].str.contains('shipping service', case=False, na=False)]['order id'].unique()
    actual_orders = df[df['type'].str.contains('order', case=False, na=False)]['order id'].unique()

    common_orders = set(returned_orders) & set(shipping_orders) & set(actual_orders)
    loss_from_returned_orders = df[df['order id'].isin(common_orders)]['total'].sum()
    print(loss_from_returned_orders)

    return (total_orders, total_cancelled_orders, total_return_orders, amazon_sharing_fees, shipping_fees, fba_fees,
            gross_profit, net_profit, total_sales, mode_value, less_than_mode, greater_than_mode, df_greater_than_mode,
            loss_from_returned_orders)


def calculate_monthly_metrics(df):
    df['date'] = pd.to_datetime(df['date/time']).dt.to_period('M')
    monthly_metrics = df.groupby('date').apply(lambda x: pd.Series({
        'total_orders': len(x[x['type'].str.contains('order', case=False, na=False)]) - len(x[x['type'].str.contains('refund|cancelled', case=False, na=False)]),
        'total_cancelled_orders': len(x[x['type'].str.contains('refund|cancelled', case=False, na=False)]),
        'amazon_sharing_fees': abs(x['selling fees'].sum()),
        'shipping_fees': abs(x['other transaction fees'].sum()),
        'fba_fees': abs(x['fba fees'].sum()),
        'total_sales': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()),
        'gross_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()),
        'net_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()) - x['total sales tax liable(gst before adjusting tcs)'].sum() - x['tcs-cgst'].sum() - x['tcs-sgst'].sum() - x['tcs-igst'].sum() - x['tds (section 194-o)'].sum(),
        'total_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()) - x['total sales tax liable(gst before adjusting tcs)'].sum() - x['tcs-cgst'].sum() - x['tcs-sgst'].sum() - x['tcs-igst'].sum() - x['tds (section 194-o)'].sum()
    })).reset_index()

    return monthly_metrics

def calculate_fulfillment_metrics(df):
    fulfillment_metrics = df.groupby('fulfillment').apply(lambda x: pd.Series({
        'total_orders': len(x[x['type'].str.contains('order', case=False, na=False)]) - len(x[x['type'].str.contains('refund|cancelled', case=False, na=False)]),
        'total_cancelled_orders': len(x[x['type'].str.contains('refund|cancelled', case=False, na=False)]),
        'amazon_sharing_fees': abs(x['selling fees'].sum()),
        'shipping_fees': abs(x['other transaction fees'].sum()),
        'fba_fees': abs(x['fba fees'].sum()),
        'total_sales': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()),
        'gross_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()),
        'net_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()) - x['total sales tax liable(gst before adjusting tcs)'].sum() - x['tcs-cgst'].sum() - x['tcs-sgst'].sum() - x['tcs-igst'].sum() - x['tds (section 194-o)'].sum(),
        'total_profit': abs(x[x['type'].str.contains('order', case=False, na=False)]['product sales'].sum()) - abs(x['selling fees'].sum()) - abs(x['other transaction fees'].sum()) - abs(x['fba fees'].sum()) - x['total sales tax liable(gst before adjusting tcs)'].sum() - x['tcs-cgst'].sum() - x['tcs-sgst'].sum() - x['tcs-igst'].sum() - x['tds (section 194-o)'].sum()
    })).reset_index()
    return fulfillment_metrics