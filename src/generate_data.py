import pandas as pd
import numpy as np

np.random.seed(42)

n_students = 1000

branches = ["CSE", "CSE-AI", "ECE", "EEE", "Mechanical", "Civil"]
years = ["2nd Year", "3rd Year", "4th Year"]
genders = ["Female", "Male"]

data = {
    "Student_ID": [f"STU{str(i).zfill(4)}" for i in range(1, n_students + 1)],
    "Branch": np.random.choice(branches, n_students),
    "Year": np.random.choice(years, n_students),
    "Gender": np.random.choice(genders, n_students),
    "Attendance": np.clip(np.random.normal(78, 12, n_students), 40, 100),
    "Previous_CGPA": np.clip(np.random.normal(7.5, 1.0, n_students), 4.0, 10.0),
    "Internal_Marks": np.clip(np.random.normal(72, 15, n_students), 30, 100),
    "Assignment_Score": np.clip(np.random.normal(75, 14, n_students), 25, 100),
    "Study_Hours": np.clip(np.random.normal(3.5, 1.8, n_students), 0.5, 10),
    "LMS_Activity": np.clip(np.random.normal(65, 20, n_students), 5, 100),
    "Library_Visits": np.clip(np.random.poisson(5, n_students), 0, 20),
    "Lab_Usage": np.clip(np.random.normal(65, 18, n_students), 10, 100),
    "Certifications": np.clip(np.random.poisson(2, n_students), 0, 8),
    "Projects": np.clip(np.random.poisson(2, n_students), 0, 7),
    "Hackathons": np.clip(np.random.poisson(1, n_students), 0, 5),
    "Internships": np.clip(np.random.poisson(1, n_students), 0, 4),
    "Commute_Time": np.clip(np.random.normal(45, 20, n_students), 5, 120),
    "Backlogs": np.clip(np.random.poisson(0.7, n_students), 0, 5),
}

df = pd.DataFrame(data)

# Generate final CGPA using several academic and engagement factors
performance_score = (
    df["Previous_CGPA"] * 0.35
    + (df["Attendance"] / 10) * 0.15
    + (df["Internal_Marks"] / 10) * 0.15
    + (df["Assignment_Score"] / 10) * 0.10
    + (df["Study_Hours"] / 10) * 0.05
    + (df["LMS_Activity"] / 100) * 1.0
    + df["Certifications"] * 0.03
    + df["Projects"] * 0.04
    - df["Backlogs"] * 0.15
    - df["Commute_Time"] * 0.002
)

df["Final_CGPA"] = np.clip(
    performance_score + np.random.normal(0, 0.35, n_students),
    4.0,
    10.0
).round(2)

# Academic status
df["Academic_Status"] = np.where(
    df["Final_CGPA"] >= 7.0,
    "Good Standing",
    np.where(
        df["Final_CGPA"] >= 5.5,
        "Needs Attention",
        "At Risk"
    )
)

# Risk level
risk_score = (
    (100 - df["Attendance"]) * 0.25
    + (10 - df["Previous_CGPA"]) * 8
    + (100 - df["Internal_Marks"]) * 0.15
    + df["Backlogs"] * 8
    + df["Commute_Time"] * 0.05
    - df["LMS_Activity"] * 0.05
)

df["Risk_Level"] = pd.cut(
    risk_score,
    bins=[-np.inf, 18, 30, np.inf],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)

# Round numerical columns
df["Attendance"] = df["Attendance"].round(2)
df["Previous_CGPA"] = df["Previous_CGPA"].round(2)
df["Internal_Marks"] = df["Internal_Marks"].round(2)
df["Assignment_Score"] = df["Assignment_Score"].round(2)
df["Study_Hours"] = df["Study_Hours"].round(2)
df["LMS_Activity"] = df["LMS_Activity"].round(2)
df["Lab_Usage"] = df["Lab_Usage"].round(2)
df["Commute_Time"] = df["Commute_Time"].round(2)

# Save dataset
df.to_csv("data/student_success_data.csv", index=False)

print("Dataset created successfully!")
print(f"Number of students: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print("\nFirst 5 records:")
print(df.head())

print("\nRisk distribution:")
print(df["Risk_Level"].value_counts())

print("\nDataset saved to:")
print("data/student_success_data.csv")