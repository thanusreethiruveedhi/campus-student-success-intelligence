import pandas as pd
import numpy as np

np.random.seed(42)

n_students = 1000

# -----------------------------
# BASIC STUDENT INFORMATION
# -----------------------------

branches = ["CSE", "CSE-AI", "ECE", "EEE", "Mechanical", "Civil"]
years = ["2nd Year", "3rd Year", "4th Year"]
genders = ["Female", "Male"]

df = pd.DataFrame({
    "Student_ID": [f"STU{str(i).zfill(4)}" for i in range(1, n_students + 1)],
    "Branch": np.random.choice(branches, n_students),
    "Year": np.random.choice(years, n_students),
    "Gender": np.random.choice(genders, n_students)
})

# -----------------------------
# ACADEMIC + ENGAGEMENT DATA
# -----------------------------

df["Attendance"] = np.clip(
    np.random.normal(80, 10, n_students), 50, 100
).round(2)

df["Previous_CGPA"] = np.clip(
    np.random.normal(7.5, 0.9, n_students), 5.0, 9.8
).round(2)

df["Internal_Marks"] = np.clip(
    np.random.normal(72, 12, n_students), 40, 100
).round(2)

df["Assignment_Score"] = np.clip(
    np.random.normal(74, 12, n_students), 40, 100
).round(2)

df["Study_Hours"] = np.clip(
    np.random.normal(4.5, 1.5, n_students), 1, 9
).round(2)

df["LMS_Activity"] = np.clip(
    np.random.normal(68, 16, n_students), 20, 100
).round(2)

df["Library_Visits"] = np.clip(
    np.random.poisson(5, n_students), 0, 15
)

df["Lab_Usage"] = np.clip(
    np.random.normal(70, 15, n_students), 20, 100
).round(2)

df["Certifications"] = np.clip(
    np.random.poisson(2, n_students), 0, 7
)

df["Projects"] = np.clip(
    np.random.poisson(2, n_students), 0, 6
)

df["Hackathons"] = np.clip(
    np.random.poisson(1, n_students), 0, 4
)

df["Internships"] = np.clip(
    np.random.poisson(1, n_students), 0, 3
)

df["Commute_Time"] = np.clip(
    np.random.normal(40, 18, n_students), 5, 100
).round(2)

# -----------------------------
# BACKLOGS
# -----------------------------

backlog_probability = np.clip(
    0.08 + (7.5 - df["Previous_CGPA"]) * 0.08,
    0.03,
    0.35
)

df["Backlogs"] = np.random.binomial(
    4,
    backlog_probability
)

# -----------------------------
# FINAL CGPA
# -----------------------------
# Designed around a realistic
# college-performance range.

final_cgpa = (
    df["Previous_CGPA"] * 0.45
    + df["Attendance"] * 0.015
    + df["Internal_Marks"] * 0.015
    + df["Assignment_Score"] * 0.010
    + df["LMS_Activity"] * 0.008
    + df["Study_Hours"] * 0.08
    + df["Projects"] * 0.05
    + df["Certifications"] * 0.03
    - df["Backlogs"] * 0.15
    - df["Commute_Time"] * 0.002
    + np.random.normal(0, 0.25, n_students)
)

df["Final_CGPA"] = np.clip(
    final_cgpa,
    5.0,
    9.8
).round(2)

# -----------------------------
# ACADEMIC STATUS
# -----------------------------

df["Academic_Status"] = np.select(
    [
        df["Final_CGPA"] >= 7.5,
        df["Final_CGPA"] >= 6.0
    ],
    [
        "Good Standing",
        "Needs Attention"
    ],
    default="At Risk"
)

# -----------------------------
# STUDENT RISK SCORE
# -----------------------------

risk_score = (
    (100 - df["Attendance"]) * 0.20
    + (8.5 - df["Previous_CGPA"]) * 5
    + (100 - df["Internal_Marks"]) * 0.12
    + df["Backlogs"] * 7
    - df["LMS_Activity"] * 0.04
    - df["Study_Hours"] * 1.2
)

# Percentile-based risk classification
risk_percentile = pd.Series(risk_score).rank(pct=True)

df["Risk_Level"] = np.select(
    [
        risk_percentile <= 0.65,
        risk_percentile <= 0.88
    ],
    [
        "Low Risk",
        "Medium Risk"
    ],
    default="High Risk"
)

# -----------------------------
# SAVE DATASET
# -----------------------------

df.to_csv(
    "data/student_success_data.csv",
    index=False
)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("=" * 60)
print("NEW DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print(f"\nStudents : {len(df)}")
print(f"Columns  : {len(df.columns)}")

print("\nAcademic Status:")
print(df["Academic_Status"].value_counts())

print("\nRisk Level:")
print(df["Risk_Level"].value_counts())

print("\nAverage Final CGPA:")
print(round(df["Final_CGPA"].mean(), 2))

print("\nAverage Attendance:")
print(round(df["Attendance"].mean(), 2))

print("\nFinal CGPA Range:")
print(
    round(df["Final_CGPA"].min(), 2),
    "to",
    round(df["Final_CGPA"].max(), 2)
)

print("\nDataset saved:")
print("data/student_success_data.csv")