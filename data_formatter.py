import pandas as pd
import os

# 1. Load the data
# The starter repo usually has 3 CSV files in a 'data' folder.
file_names = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv",
]
dataframes = []

for file in file_names:
    if os.path.exists(file):
        df = pd.read_csv(file)
        dataframes.append(df)

# Combine them into one large dataframe
merged_df = pd.concat(dataframes, ignore_index=True)

# 2. Filter for only 'Pink Morsels'
filtered_df = merged_df[merged_df["product"] == "pink morsel"].copy()

# 3. Clean the 'price' column (remove the '$' symbol and convert to a number)
filtered_df["price"] = filtered_df["price"].str.replace("$", "").astype(float)

# 4. Calculate the total 'sales' (quantity * price)
filtered_df["sales"] = filtered_df["quantity"] * filtered_df["price"]

# 5. Keep only the requested columns: sales, date, region
final_df = filtered_df[["sales", "date", "region"]]

# 6. Save the clean data to a new CSV file
final_df.to_csv("formatted_sales_data.csv", index=False)
print("Data successfully cleaned and saved to formatted_sales_data.csv!")
