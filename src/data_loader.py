import pandas as pd
import numpy as np

def load_data(file):
    df = pd.read_csv(file)
    df.columns = [col.strip().lower() for col in df.columns]
    
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
    
    df = order_reconciliation(df)
    
    return df

def order_reconciliation(df):
    """
    Adds a new column 'estimated_selling_commission' to the DataFrame.
    
    Calculation:
    estimated_selling_commission = round(abs(selling fees * 100 / (1.18 * (product sales + total sales tax))))
    This calculation is only applied to rows where 'type' contains 'order'.
    
    Args:
    df (pd.DataFrame): DataFrame containing the order data.

    Returns:
    pd.DataFrame: DataFrame with the new 'estimated_selling_commission' column.
    """
    # Ensure necessary columns are numeric
    df['selling fees'] = pd.to_numeric(df['selling fees'], errors='coerce').fillna(0)
    df['product sales'] = pd.to_numeric(df['product sales'], errors='coerce').fillna(0)
    df['total sales tax liable(gst before adjusting tcs)'] = pd.to_numeric(df['total sales tax liable(gst before adjusting tcs)'], errors='coerce').fillna(0)
    
    # Initialize the new column with NaN
    df['estimated_selling_commission'] = np.nan
    
    # Apply the calculation only to rows where 'type' contains 'order'
    mask = df['type'].str.contains('order', case=False, na=False)
    df.loc[mask, 'estimated_selling_commission'] = np.round(
        abs(df['selling fees'][mask] * 100 / (1.18 * (df['product sales'][mask] + df['total sales tax liable(gst before adjusting tcs)'][mask]))),
        2
    )
    
    return df
