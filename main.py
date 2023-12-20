import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('concatenated_file.csv')

# Identify numeric columns
numeric_columns = df.select_dtypes(include='number').columns

# Convert numeric columns to float
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Round numeric columns to 4 decimal places
df[numeric_columns] = df[numeric_columns].round(15)

# Save the DataFrame with the updated values to a new CSV file
df.to_csv('your_updated_file.csv', index=False)
