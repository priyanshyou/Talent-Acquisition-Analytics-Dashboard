import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("HR_Job_Placement_Cleaned.csv")
sns.set(style="whitegrid")

plt.figure(figsize=(6,4))
sns.countplot(x='competition_level', hue='status', data=df)
plt.title("Competition Level vs Job Acceptance")
plt.xlabel("Competition Level")
plt.ylabel("Count")
plt.show()
