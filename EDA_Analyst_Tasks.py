import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =============================
# 1. LOAD DATASET
# =============================
df = pd.read_csv("HR_Job_Placement_Feature_Engineered.csv")
df.columns = df.columns.str.lower()

print("\n✅ Dataset loaded successfully")
print(f"Total rows: {df.shape[0]}")
print(f"Total columns: {df.shape[1]}")

# =============================
# 2. SMART COLUMN FINDER (SAFE)
# =============================
def find_col(possible_names):
    for col in possible_names:
        if col in df.columns:
            print(f"✔ Using column: {col}")
            return col
    print(f"⚠ Column not found from: {possible_names}")
    return None

# Try to map commonly expected columns
status_col = find_col(["status", "placement_status"])
degree_col = find_col(["degree_percentage", "degree_p", "degree_percent"])
interview_col = find_col([
    "interview_score",
    "interviewmarks",
    "interview_rating",
    "interview_performance",
    "technical_score"
])
skills_col = find_col([
    "skills_match_percentage",
    "skills_match",
    "skill_match",
    "skills_score"
])

# =============================
# 3. BASIC DATA CHECK
# =============================
print("\n🔹 First 5 rows:")
print(df.head())

print("\n🔹 Missing values summary:")
print(df.isnull().sum())

# =============================
# 4. EDA: PLACEMENT VS DEGREE
# =============================
if status_col and degree_col:
    print("\n🔹 Degree Percentage vs Placement Status")
    print(df.groupby(status_col)[degree_col].mean())

    plt.figure(figsize=(6, 4))
    sns.boxplot(x=status_col, y=degree_col, data=df)
    plt.title("Degree Percentage vs Placement Status")
    plt.tight_layout()
    plt.show()
else:
    print("⚠ Skipping Degree vs Placement EDA")

# =============================
# 5. EDA: INTERVIEW SCORE
# =============================
if interview_col:
    print("\n🔹 Interview Score Summary")
    print(df[interview_col].describe())

    plt.figure(figsize=(6, 4))
    sns.histplot(df[interview_col], bins=10, kde=True)
    plt.title("Interview Score Distribution")
    plt.tight_layout()
    plt.show()
else:
    print("⚠ Skipping Interview Score EDA")

# =============================
# 6. EDA: SKILLS MATCH
# =============================
if skills_col and status_col:
    print("\n🔹 Skills Match vs Placement Status")
    print(df.groupby(status_col)[skills_col].mean())

    plt.figure(figsize=(6, 4))
    sns.boxplot(x=status_col, y=skills_col, data=df)
    plt.title("Skills Match vs Placement Status")
    plt.tight_layout()
    plt.show()
else:
    print("⚠ Skipping Skills Match EDA")

# =============================
# 7. CORRELATION (NUMERIC ONLY)
# =============================
print("\n🔹 Correlation Matrix (Numeric Features)")
numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:
    corr = numeric_df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=False, cmap="coolwarm")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.show()
else:
    print("⚠ No numeric columns for correlation")

# =============================
# 8. EDA COMPLETE
# =============================
print("\n✅ EDA Analysis Completed Successfully")
