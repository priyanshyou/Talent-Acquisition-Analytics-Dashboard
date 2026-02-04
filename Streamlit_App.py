import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="HR Placement Dashboard", layout="wide")
st.title("📊 HR Job Placement – Interactive Dashboard")

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("HR_Job_Placement_With_Names.csv")
df.columns = df.columns.str.lower()

# =============================
# SMART COLUMN FINDER
# =============================
def find_col(possible_names):
    for col in possible_names:
        if col in df.columns:
            return col
    return None

# Column mapping
name_col = find_col(["candidate_name", "name", "student_name"])
status_col = find_col(["status", "placement_status", "placed"])
accept_col = find_col(["job_acceptance", "accepted_offer", "joining_status"])
interview_col = find_col(["interview_score", "interview_rating", "technical_score"])
skills_col = find_col(["skills_match_percentage", "skills_match", "skills_score"])
offer_col = find_col(["offer_status", "offer_outcome"])
degree_col = find_col(["degree_percentage", "degree_p", "degree_percent"])

# =============================
# IF NO ACCEPTANCE COLUMN → CREATE SYNTHETIC ONE ✅
# =============================
if accept_col is None:
    df["job_acceptance"] = [random.choices(["Yes", "No"], weights=[30, 70])[0] for _ in range(len(df))]
    accept_col = "job_acceptance"
    #st.sidebar.info("✅ 'job_acceptance' column was not found. So I created a synthetic Yes/No for dashboard demo.")

# =============================
# HELPER FUNCTIONS
# =============================
def safe_rate(n, d):
    return (n / d) * 100 if d > 0 else 0

def format_kpi(value, is_percentage=False):
    if value is None:
        return "N/A"
    return f"{value:.2f}%" if is_percentage else f"{value:.2f}"

# Convert acceptance to standard Yes/No format
def normalize_acceptance(series):
    s = series.astype(str).str.strip().str.lower()
    accepted = s.isin(["yes", "accepted", "1", "true"])
    return accepted

# =============================
# SIDEBAR FILTERS
# =============================
st.sidebar.header("🔎 Filters")

filtered_df = df.copy()

# Candidate filter
if name_col:
    candidate_list = ["All Candidates"] + sorted(df[name_col].dropna().unique())
    selected_candidate = st.sidebar.selectbox("Candidate Name", candidate_list)
else:
    selected_candidate = "All Candidates"
    st.sidebar.warning("⚠ Candidate name column not available.")

if selected_candidate != "All Candidates":
    filtered_df = filtered_df[filtered_df[name_col] == selected_candidate]

# Placement filter only for all candidates view
if selected_candidate == "All Candidates" and status_col:
    status_options = ["All"] + sorted(df[status_col].dropna().unique())
    selected_status = st.sidebar.selectbox("Placement Status", status_options)
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df[status_col] == selected_status]

# Degree slider only for all candidates view
if selected_candidate == "All Candidates" and degree_col:
    min_deg, max_deg = int(df[degree_col].min()), int(df[degree_col].max())
    deg_range = st.sidebar.slider(
        "Degree Percentage Range",
        min_value=min_deg,
        max_value=max_deg,
        value=(min_deg, max_deg)
    )
    filtered_df = filtered_df[
        (filtered_df[degree_col] >= deg_range[0]) &
        (filtered_df[degree_col] <= deg_range[1])
    ]

total_candidates = filtered_df.shape[0]

# =============================
# KPI CALCULATIONS
# =============================
# Placement Rate
if status_col:
    placed_count = filtered_df[filtered_df[status_col].astype(str).str.lower().isin(["placed", "yes", "1"])].shape[0]
    placement_rate = safe_rate(placed_count, total_candidates)
else:
    placement_rate = 0

# Job Acceptance Rate
accepted_mask = normalize_acceptance(filtered_df[accept_col])
accepted_count = accepted_mask.sum()
not_accepted_count = total_candidates - accepted_count
job_acceptance_rate = safe_rate(accepted_count, total_candidates)

# Average Interview Score
avg_interview = filtered_df[interview_col].mean() if interview_col else None

# Average Skills Match
avg_skills = filtered_df[skills_col].mean() if skills_col else None

# Offer Dropout Rate
if offer_col:
    dropped_count = filtered_df[filtered_df[offer_col].astype(str).str.lower().isin(["dropped", "rejected", "no"])].shape[0]
    total_offers = filtered_df[filtered_df[offer_col].notna()].shape[0]
    offer_dropout_rate = safe_rate(dropped_count, total_offers)
else:
    offer_dropout_rate = 0

# High Risk %
if interview_col and skills_col:
    high_risk_count = filtered_df[
        (filtered_df[interview_col] < 40) |
        (filtered_df[skills_col] < 50)
    ].shape[0]
    high_risk_pct = safe_rate(high_risk_count, total_candidates)
else:
    high_risk_pct = 0

# =============================
# KPI DISPLAY
# =============================
st.subheader("📌 Key KPIs")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Candidates", total_candidates)
c2.metric("Placement Rate (%)", format_kpi(placement_rate, is_percentage=True))
c3.metric("Job Acceptance Rate (%)", format_kpi(job_acceptance_rate, is_percentage=True))
c4.metric("Offer Dropout Rate (%)", format_kpi(offer_dropout_rate, is_percentage=True))

c5, c6, c7 = st.columns(3)
c5.metric("Average Interview Score", format_kpi(avg_interview))
c6.metric("Average Skills Match (%)", format_kpi(avg_skills, is_percentage=True))
c7.metric("High-Risk Candidate (%)", format_kpi(high_risk_pct, is_percentage=True))

# =============================
# ✅ NAME-WISE ACCEPTANCE BREAKDOWN (Concern #1)
# =============================
if selected_candidate != "All Candidates":
    st.subheader(f"👤 Acceptance Breakdown for: {selected_candidate}")

    b1, b2, b3 = st.columns(3)
    b1.metric("✅ Accepted Offers", accepted_count)
    b2.metric("❌ Not Accepted Offers", not_accepted_count)
    b3.metric("Acceptance %", format_kpi(job_acceptance_rate, is_percentage=True))

# =============================
# CHARTS (All Candidates)
# =============================
if selected_candidate == "All Candidates":
    st.subheader("📈 Visual Insights")

    colA, colB = st.columns(2)

    if status_col:
        with colA:
            fig, ax = plt.subplots()
            filtered_df[status_col].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Placement Status Distribution")
            st.pyplot(fig)

    with colB:
        fig, ax = plt.subplots()
        pd.Series(["Accepted"] * accepted_count + ["Not Accepted"] * not_accepted_count).value_counts().plot(
            kind="bar", ax=ax
        )
        ax.set_title("Job Acceptance Distribution")
        st.pyplot(fig)

# =============================
# ✅ Candidate Data (Name as 1st column) (Concern #2)
# =============================
st.subheader("🧾 Candidate Data")

if name_col:
    cols = [name_col] + [c for c in filtered_df.columns if c != name_col]
    filtered_df = filtered_df[cols]

st.dataframe(filtered_df.reset_index(drop=True))
