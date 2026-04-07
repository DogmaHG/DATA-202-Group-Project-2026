import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# ==========================================
# 1. LOADING & CLEANING
# ==========================================
print("--- Loading Data ---")
# Adjust the filename if yours is still 'Movies_and_TV.csv'
column_names = ['item_id', 'user_id', 'rating', 'timestamp']
# This takes a random 10% of your data (still ~87k rows, which is plenty!)
df = pd.read_csv("Movies_and_TV.csv", header=None, names=column_names).sample(frac=0.1, random_state=42)

# Convert timestamp to readable date
df['date'] = pd.to_datetime(df['timestamp'], unit='s')

# Create the Target Variable: 1 if rating >= 4 (Liked), 0 otherwise (Disliked)
df['liked'] = (df['rating'] >= 4).astype(int)

# ==========================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================
print("\n--- Data Insights ---")
print(f"Total Reviews: {len(df)}")
print(f"Average Rating: {df['rating'].mean():.2f}")
print(f"Missing Values:\n{df.isnull().sum()}")

# Quick check on the balance of our target (How many liked vs disliked?)
print("\nTarget Distribution (Liked vs Disliked):")
print(df['liked'].value_counts(normalize=True))

# ==========================================
# 3. FEATURE ENGINEERING
# ==========================================
print("\n--- Preparing Features ---")
# Machine Learning models need numbers, not strings. 
# LabelEncoder converts 'A3478...' into a number like 102.
le_user = LabelEncoder()
le_item = LabelEncoder()

df['user_encoded'] = le_user.fit_transform(df['user_id'])
df['item_encoded'] = le_item.fit_transform(df['item_id'])

# Define our features (X) and what we want to predict (y)
X = df[['user_encoded', 'item_encoded']]
y = df['liked']

# ==========================================
# 4. RANDOM FOREST MODEL
# ==========================================
print("\n--- Training Random Forest ---")
# Split data: 80% to train the model, 20% to test how well it learned
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Classifier
# n_estimators=100 means we are building 100 individual decision trees
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# ==========================================
# 5. RESULTS & EVALUATION
# ==========================================
predictions = rf_model.predict(X_test)

print("\n--- Model Performance ---")
print(f"Accuracy Score: {accuracy_score(y_test, predictions):.2%}")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Quick example: Predicting if User #10 would like Item #50
# example_pred = rf_model.predict([[10, 50]])