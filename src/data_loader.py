import pandas as pd

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
    
    return df
