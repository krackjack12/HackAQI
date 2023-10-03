import pandas as pd

# Replace 'input.csv' with the path to your CSV file.
csv_file_path = 'routesdata.csv'

# Read the CSV file into a Pandas DataFrame.
df = pd.read_csv(csv_file_path)

# Remove duplicates based on the 'stop_name' column.
df_cleaned = df.drop_duplicates()

# Save the cleaned DataFrame to a new CSV file if needed.
# Replace 'output.csv' with the desired output file path.
output_csv_file = 'routesdata2.csv'
df_cleaned.to_csv(output_csv_file, index=False)

# Print the cleaned DataFrame (optional).
print(df_cleaned)
