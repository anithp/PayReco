import pandas as pd

# Load the CSV files
file1_path = '/Users/anith/Documents/GitHub/PayReco/Data/All orders.xlsx - Sheet1.csv'
file2_path = '/Users/anith/Documents/GitHub/PayReco/Data/drr.csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Display the first few rows of each file
df1_head = df1.head()
df2_head = df2.head()

print(df1_head)
print(df2_head)
