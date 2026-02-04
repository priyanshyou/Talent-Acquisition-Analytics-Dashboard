# ---------------------------------------------
# HR Job Placement - Feature Engineering
# ---------------------------------------------
# Author: Diviya
# Description:
# This script creates derived analytical features for job acceptance prediction.
# ---------------------------------------------

import pandas as pd
import numpy as np

# -----------------------------
# Step 1: Load cleaned dataset
# -----------------------------
df = pd.read_csv("HR_Job_Placement_Cleaned.csv")

print("Dataset loaded successfully")
print("Shape:", df.shape)

# -----------------------------
# Step 2: Experience Category
# -----------------------------
def experience_category(exp):
    if exp == 0:
        return "Fresher"
    elif exp <= 3:
        return "Junior"
    else:
        return "Senior"

df["experience_category"] = df["years_of_experience"].apply(experience_category)

# -----------------------------
# Step 3: Academic Performance Bands
# -----------------------------
df["academic_avg"] = (
    df["ssc_percentage"] +
    df["hsc_percentage"] +
    df["degree_percentage"]
) / 3

def academic_band(score):
    if score < 60:
        return "Low"
    elif score <= 75:
        return "Medium"
    else:
        return "High"

df["academic_performance_band"] = df["academic_avg"].apply(academic_band)

# -----------------------------
# Step 4: Skills Match Level
# -----------------------------
def skills_level(score):
    if score < 50:
        return "Low"
    elif score <= 75:
        return "Medium"
    else:
        return "High"

df["skills_match_level"] = df["skills_match_percentage"].apply(skills_level)

# -----------------------------
# Step 5: Interview Performance Category
# -----------------------------
df["interview_avg_score"] = (
    df["technical_score"] +
    df["aptitude_score"] +
    df["communication_score"]
) / 3

def interview_category(score):
    if score < 60:
        return "Poor"
    elif score <= 75:
        return "Average"
    else:
        return "Excellent"

df["interview_performance_category"] = df["interview_avg_score"].apply(interview_category)

# -----------------------------
# Step 6: Placement Probability Score (Rule-based)
# -----------------------------
df["placement_probability_score"] = (
    0.3 * (df["skills_match_level"] == "High").astype(int) +
    0.4 * (df["interview_performance_category"] == "Excellent").astype(int) +
    0.2 * (df["experience_category"] == "Senior").astype(int) +
    0.1 * (df["academic_performance_band"] == "High").astype(int)
)

# -----------------------------
# Step 7: Final Check
# -----------------------------
print("\nNew engineered features added:")
print([
    "experience_category",
    "academic_performance_band",
    "skills_match_level",
    "interview_performance_category",
    "placement_probability_score"
])

# -----------------------------
# Step 8: Save Feature-Engineered Dataset
# -----------------------------
output_file = "HR_Job_Placement_Feature_Engineered.csv"
df.to_csv(output_file, index=False)

print("\nFeature engineering completed successfully!")
print(f"Saved as: {output_file}")
