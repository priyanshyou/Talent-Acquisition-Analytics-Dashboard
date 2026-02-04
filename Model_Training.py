import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# =============================
# 1. LOAD DATA
# =============================
df = pd.read_csv("HR_Job_Placement_Feature_Engineered.csv")
df.columns = df.columns.str.lower()

print("\n✅ Dataset Loaded")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# =============================
# 2. SAFE COLUMN FINDER
# =============================
def find_col(possible_names):
    for col in possible_names:
        if col in df.columns:
            print(f"✔ Using column: {col}")
            return col
    print(f"⚠ None found from: {possible_names}")
    return None

# =============================
# 3. TARGET COLUMN DETECTION
# =============================
target_col = find_col([
    "job_acceptance",
    "accepted_offer",
    "offer_acceptance",
    "final_decision",
    "joining_status",
    "placed",
    "status",
    "target",
    "label"
])

if not target_col:
    raise ValueError("❌ No suitable target column found for model training")

# =============================
# 4. FEATURE COLUMNS
# =============================
interview_col = find_col([
    "interview_score",
    "interview_rating",
    "technical_score"
])

skills_col = find_col([
    "skills_match_percentage",
    "skills_match",
    "skills_score"
])

degree_col = find_col([
    "degree_percentage",
    "degree_p",
    "degree_percent"
])

features = [c for c in [interview_col, skills_col, degree_col] if c]

if len(features) < 2:
    raise ValueError("❌ Not enough feature columns for training")

X = df[features]

# =============================
# 5. TARGET ENCODING (SAFE)
# =============================
y_raw = df[target_col]

if y_raw.dtype == "object":
    y = y_raw.map({
        "yes": 1,
        "placed": 1,
        "accepted": 1,
        "no": 0,
        "not placed": 0,
        "rejected": 0
    })
else:
    y = y_raw

# Drop rows with unmapped target
mask = y.notna()
X = X[mask]
y = y[mask]

# =============================
# 6. TRAIN MODEL
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)

print("\n✅ Model Training Completed")
print("Accuracy:", accuracy_score(y_test, preds))
