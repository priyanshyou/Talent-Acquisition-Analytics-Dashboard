import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("HR_Job_Placement_Cleaned.csv")
sns.set(style="whitegrid")

plt.figure(figsize=(6,4))
sns.countplot(x='company_tier', hue='status', data=df)
plt.title("Company Tier vs Job Acceptance")
plt.xlabel("Company Tier")
plt.ylabel("Count")
plt.show()
