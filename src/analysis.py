import pandas as pd
import numpy as np
import os

print("=" * 60)
print("DATA CLEANING + EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# 1. LOAD RAW DATA
# --------------------------------------------------

input_file = "data/student_success_data.csv"
clean_file = "data/student_success_clean.csv"

df = pd.read_csv(input_file)

print("\nRAW DATA")
print("-" * 40)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

# --------------------------------------------------
# 2. DATA TYPES
# --------------------------------------------------

print("\nDATA TYPES")
print("-" * 40)

print(df.dtypes)

# --------------------------------------------------
# 3. MISSING VALUES
# --------------------------------------------------

print("\nMISSING VALUES")
print("-" * 40)

missing_values = df.isnull().sum()

print(missing_values)

# --------------------------------------------------
# 4. DUPLICATES
# --------------------------------------------------

print("\nDUPLICATE RECORDS")
print("-" * 40)

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)

# Remove duplicates if any
df = df.drop_duplicates()

# --------------------------------------------------
# 5. DUPLICATE STUDENT IDs
# --------------------------------------------------

duplicate_ids = df["Student_ID"].duplicated().sum()

print("Duplicate Student IDs:", duplicate_ids)

# --------------------------------------------------
# 6. BASIC VALIDATION
# --------------------------------------------------

print("\nDATA VALIDATION")
print("-" * 40)

print(
    "Attendance range:",
    df["Attendance"].min(),
    "to",
    df["Attendance"].max()
)

print(
    "Previous CGPA range:",
    df["Previous_CGPA"].min(),
    "to",
    df["Previous_CGPA"].max()
)

print(
    "Final CGPA range:",
    df["Final_CGPA"].min(),
    "to",
    df["Final_CGPA"].max()
)

# --------------------------------------------------
# 7. SAVE CLEAN DATA
# --------------------------------------------------

df.to_csv(clean_file, index=False)

print("\nClean dataset saved:")
print(clean_file)

# ==================================================
# EXPLORATORY DATA ANALYSIS
# ==================================================

print("\n")
print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# 8. KEY PERFORMANCE INDICATORS
# --------------------------------------------------

print("\nKEY PERFORMANCE INDICATORS")
print("-" * 40)

total_students = len(df)

average_cgpa = df["Final_CGPA"].mean()

average_attendance = df["Attendance"].mean()

high_risk = (df["Risk_Level"] == "High Risk").sum()

print(f"Total Students       : {total_students}")
print(f"Average Final CGPA   : {average_cgpa:.2f}")
print(f"Average Attendance   : {average_attendance:.2f}%")
print(f"High-Risk Students   : {high_risk}")

# --------------------------------------------------
# 9. BRANCH PERFORMANCE
# --------------------------------------------------

print("\nBRANCH PERFORMANCE")
print("-" * 40)

branch_performance = (
    df.groupby("Branch")
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance", "mean")
    )
    .round(2)
)

high_risk_by_branch = (
    df[df["Risk_Level"] == "High Risk"]
    .groupby("Branch")
    .size()
    .rename("High_Risk")
)

branch_performance = branch_performance.join(
    high_risk_by_branch,
    how="left"
)

branch_performance["High_Risk"] = (
    branch_performance["High_Risk"]
    .fillna(0)
    .astype(int)
)

print(branch_performance)

# --------------------------------------------------
# 10. ACADEMIC STATUS
# --------------------------------------------------

print("\nACADEMIC STATUS")
print("-" * 40)

print(df["Academic_Status"].value_counts())

# --------------------------------------------------
# 11. RISK DISTRIBUTION
# --------------------------------------------------

print("\nRISK DISTRIBUTION")
print("-" * 40)

print(df["Risk_Level"].value_counts())

# --------------------------------------------------
# 12. CORRELATION ANALYSIS
# --------------------------------------------------

print("\nCORRELATION WITH FINAL CGPA")
print("-" * 40)

numeric_columns = df.select_dtypes(
    include=np.number
)

correlation = (
    numeric_columns
    .corr()["Final_CGPA"]
    .sort_values(ascending=False)
)

print(correlation.round(3))

# --------------------------------------------------
# 13. RESOURCE USAGE
# --------------------------------------------------

print("\nRESOURCE USAGE")
print("-" * 40)

resource_usage = pd.DataFrame({
    "Resource": [
        "LMS Activity",
        "Library Visits",
        "Lab Usage",
        "Projects",
        "Certifications",
        "Hackathons",
        "Internships"
    ],
    "Average": [
        df["LMS_Activity"].mean(),
        df["Library_Visits"].mean(),
        df["Lab_Usage"].mean(),
        df["Projects"].mean(),
        df["Certifications"].mean(),
        df["Hackathons"].mean(),
        df["Internships"].mean()
    ]
})

resource_usage["Average"] = resource_usage["Average"].round(2)

print(resource_usage)

# --------------------------------------------------
# 14. RISK BY BRANCH
# --------------------------------------------------

print("\nRISK BY BRANCH")
print("-" * 40)

risk_by_branch = pd.crosstab(
    df["Branch"],
    df["Risk_Level"]
)

print(risk_by_branch)

# --------------------------------------------------
# 15. ATTENDANCE GROUP ANALYSIS
# --------------------------------------------------

print("\nATTENDANCE GROUP ANALYSIS")
print("-" * 40)

df["Attendance_Group"] = pd.cut(
    df["Attendance"],
    bins=[0, 60, 75, 85, 100],
    labels=[
        "Below 60%",
        "60-75%",
        "75-85%",
        "Above 85%"
    ]
)

attendance_analysis = (
    df.groupby("Attendance_Group", observed=True)
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean")
    )
    .round(2)
)

print(attendance_analysis)

# --------------------------------------------------
# 16. BACKLOG ANALYSIS
# --------------------------------------------------

print("\nBACKLOG ANALYSIS")
print("-" * 40)

backlog_analysis = (
    df.groupby("Backlogs")
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean")
    )
    .round(2)
)

print(backlog_analysis)

# --------------------------------------------------
# 17. SAVE ANALYSIS TABLES
# --------------------------------------------------

branch_performance.to_csv(
    "data/branch_performance.csv"
)

resource_usage.to_csv(
    "data/resource_usage.csv",
    index=False
)

risk_by_branch.to_csv(
    "data/risk_by_branch.csv"
)

attendance_analysis.to_csv(
    "data/attendance_analysis.csv"
)

backlog_analysis.to_csv(
    "data/backlog_analysis.csv"
)

print("\nAnalysis tables saved successfully.")

# --------------------------------------------------
# 18. FINAL MESSAGE
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA CLEANING + EDA COMPLETED SUCCESSFULLY")
print("=" * 60)