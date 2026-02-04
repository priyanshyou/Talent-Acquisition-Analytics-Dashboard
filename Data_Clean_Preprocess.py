# HR Job Placement - Data Cleaning & Preprocessing
# ------------------------------------------------
# Author: Diviya
# Description:
# This script performs data cleaning and preprocessing
# on the HR Job Placement Dataset.

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# -----------------------------
# Step 1: Load Dataset
# -----------------------------
file_path = "HR_Job_Placement_Dataset.csv"
df = pd.read_csv("HR_Job_Placement_Dataset.csv")

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

# -----------------------------
# Step 2: Initial Inspection
# -----------------------------
print("\nDataset Info:")
print(df.info())

# -----------------------------
# Step 3: Handling Missing Values
# -----------------------------

# Numerical columns - Mean / Median
df['ssc_percentage'] = df['ssc_percentage'].fillna(df['ssc_percentage'].mean())
df['hsc_percentage'] = df['hsc_percentage'].fillna(df['hsc_percentage'].mean())
df['employment_gap_months'] = df['employment_gap_months'].fillna(
    df['employment_gap_months'].median()
)

# Categorical columns - Mode
df['layoff_history'] = df['layoff_history'].fillna(
    df['layoff_history'].mode()[0]
)
df['relocation_willingness'] = df['relocation_willingness'].fillna(
    df['relocation_willingness'].mode()[0]
)

print("\nMissing values handled successfully")

# -----------------------------
# Step 4: Fixing Inconsistent Labels
# -----------------------------
df['gender'] = df['gender'].str.strip().str.title()
df['status'] = df['status'].str.strip().str.title()

print("Categorical labels standardized")

# -----------------------------
# Step 5: Encoding Categorical Variables
# -----------------------------

# Label Encoding for target variable
le = LabelEncoder()
df['status'] = le.fit_transform(df['status'])  # Placed=1, Not Placed=0

# One-Hot Encoding for other categorical columns
df = pd.get_dummies(
    df,
    columns=['degree_specialization', 'gender'],
    drop_first=True
)

print("Categorical variables encoded")

# -----------------------------
# Step 6: Feature Scaling
# -----------------------------
scaler = StandardScaler()

num_cols = [
    'ssc_percentage',
    'hsc_percentage',
    'degree_percentage',
    'technical_score',
    'aptitude_score',
    'communication_score'
]

df[num_cols] = scaler.fit_transform(df[num_cols])

print("Numerical features scaled")

# -----------------------------
# Step 7: Final Check
# -----------------------------
print("\nTotal missing values after cleaning:", df.isnull().sum().sum())

# -----------------------------
# Step 8: Save Cleaned Dataset
# -----------------------------
output_file = "HR_Job_Placement_Cleaned.csv"
df.to_csv(output_file, index=False)

print("\nData cleaning and preprocessing completed successfully!")
print(f"Cleaned dataset saved as: {output_file}")
