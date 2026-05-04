import pandas as pd
import matplotlib.pyplot as plt

# List of column names (adjust these if you know the actual names!)
cols = ['user_id', 'item_id', 'rating', 'timestamp']

# Load the file without an existing header and assign names
df = pd.read_csv('Movies_and_TV.csv', names=cols, header=None)

# Now check the first 5 rows again
print(df.head())

#Missing Data
print(df.isnull().sum())

#Converting to readable dates
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
print(df.head())



# 1. Load data (using your previous setup)
cols = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('Movies_and_TV.csv', names=cols, header=None)

# 2. Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# 3. Extract the month and month name for analysis
df['month'] = df['timestamp'].dt.month
df['month_name'] = df['timestamp'].dt.month_name()

# 4. Calculate the average rating per month
seasonal_data = df.groupby('month')['rating'].mean()
month_labels = df.groupby('month')['month_name'].first()

# 5. Plot the results
plt.figure(figsize=(10, 5))
plt.plot(month_labels, seasonal_data, marker='o', color='b', linestyle='-')

plt.title('Average Movie/TV Ratings by Month')
plt.xlabel('Month')
plt.ylabel('Average Rating')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Optional: Print the raw numbers to the terminal
print("Average Rating per Month:")
print(df.groupby('month_name')['rating'].mean().sort_values(ascending=False))