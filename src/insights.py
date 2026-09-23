import pandas as pd
import numpy as np

print("=" * 70)
print("BUSINESS INSIGHTS ANALYSIS")
print("=" * 70)

# Load cleaned dataset
df = pd.read_csv("data/student_success_clean.csv")

# ============================================================
# CREATE ATTENDANCE GROUP
# ============================================================

df["Attendance_Group"] = pd.cut(
    df["Attendance"],
    bins=[0, 60, 75, 85, 100],
    labels=[
        "Below 60%",
        "60-75%",
        "75-85%",
        "Above 85%"
    ],
    include_lowest=True
)

# ============================================================
# 1. ACADEMIC PERFORMANCE
# ============================================================

print("\n1. ACADEMIC PERFORMANCE")
print("-" * 50)

average_final_cgpa = df["Final_CGPA"].mean()
average_previous_cgpa = df["Previous_CGPA"].mean()
average_change = average_final_cgpa - average_previous_cgpa

print(f"Average Final CGPA: {average_final_cgpa:.2f}")
print(f"Average Previous CGPA: {average_previous_cgpa:.2f}")
print(f"Average CGPA Change: {average_change:.2f}")

# ============================================================
# 2. ATTENDANCE AND ACADEMIC PERFORMANCE
# ============================================================

print("\n2. ATTENDANCE AND ACADEMIC PERFORMANCE")
print("-" * 50)

attendance_groups = (
    df.groupby("Attendance_Group", observed=True)
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean")
    )
    .round(2)
)

print(attendance_groups)

attendance_groups.to_csv(
    "data/attendance_insights.csv"
)

# ============================================================
# 3. BACKLOGS AND ACADEMIC PERFORMANCE
# ============================================================

print("\n3. BACKLOGS AND ACADEMIC PERFORMANCE")
print("-" * 50)

backlog_analysis = (
    df.groupby("Backlogs")
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance", "mean")
    )
    .round(2)
)

print(backlog_analysis)

backlog_analysis.to_csv(
    "data/backlog_insights.csv"
)

# ============================================================
# 4. BRANCH PERFORMANCE
# ============================================================

print("\n4. BRANCH PERFORMANCE")
print("-" * 50)

branch_insights = (
    df.groupby("Branch")
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance", "mean"),
        Average_LMS_Activity=("LMS_Activity", "mean"),
        Average_Study_Hours=("Study_Hours", "mean"),
        High_Risk_Students=(
            "Risk_Level",
            lambda x: (x == "High Risk").sum()
        )
    )
    .round(2)
)

print(branch_insights)

branch_insights.to_csv(
    "data/branch_insights.csv"
)

# ============================================================
# 5. STUDENT ENGAGEMENT
# ============================================================

print("\n5. STUDENT ENGAGEMENT AND ACADEMIC PERFORMANCE")
print("-" * 50)

engagement_columns = [
    "Attendance",
    "LMS_Activity",
    "Library_Visits",
    "Lab_Usage",
    "Certifications",
    "Projects",
    "Hackathons",
    "Internships",
    "Study_Hours",
    "Assignment_Score"
]

engagement_correlation = (
    df[engagement_columns + ["Final_CGPA"]]
    .corr()["Final_CGPA"]
    .drop("Final_CGPA")
    .sort_values(ascending=False)
    .round(3)
)

print(engagement_correlation)

engagement_correlation_df = engagement_correlation.reset_index()

engagement_correlation_df.columns = [
    "Factor",
    "Correlation_With_Final_CGPA"
]

engagement_correlation_df.to_csv(
    "data/engagement_correlation.csv",
    index=False
)

# ============================================================
# 6. LMS ENGAGEMENT
# ============================================================

print("\n6. LMS ENGAGEMENT GROUPS")
print("-" * 50)

df["LMS_Group"] = pd.cut(
    df["LMS_Activity"],
    bins=[0, 40, 70, 100],
    labels=[
        "Low LMS Activity",
        "Medium LMS Activity",
        "High LMS Activity"
    ],
    include_lowest=True
)

lms_insights = (
    df.groupby("LMS_Group", observed=True)
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance", "mean"),
        Average_Study_Hours=("Study_Hours", "mean")
    )
    .round(2)
)

print(lms_insights)

lms_insights.to_csv(
    "data/lms_insights.csv"
)

# ============================================================
# 7. STUDENTS NEEDING SUPPORT
# ============================================================

print("\n7. STUDENTS NEEDING ACADEMIC SUPPORT")
print("-" * 50)

support_students = df[
    (df["Risk_Level"] == "High Risk") |
    (df["Academic_Status"] == "At Risk")
]

print(f"Students flagged for support: {len(support_students)}")

support_by_branch = (
    support_students
    .groupby("Branch")
    .size()
    .sort_values(ascending=False)
)

print("\nSupport Students by Branch:")
print(support_by_branch)

# ============================================================
# 8. HIGH-RISK STUDENT PROFILE
# ============================================================

print("\n8. HIGH-RISK STUDENT PROFILE")
print("-" * 50)

high_risk = df[
    df["Risk_Level"] == "High Risk"
]

high_risk_profile = pd.DataFrame({
    "Metric": [
        "Number of High-Risk Students",
        "Average Attendance",
        "Average Previous CGPA",
        "Average Final CGPA",
        "Average Internal Marks",
        "Average Assignment Score",
        "Average LMS Activity",
        "Average Study Hours",
        "Average Backlogs",
        "Average Commute Time"
    ],
    "Value": [
        len(high_risk),
        high_risk["Attendance"].mean(),
        high_risk["Previous_CGPA"].mean(),
        high_risk["Final_CGPA"].mean(),
        high_risk["Internal_Marks"].mean(),
        high_risk["Assignment_Score"].mean(),
        high_risk["LMS_Activity"].mean(),
        high_risk["Study_Hours"].mean(),
        high_risk["Backlogs"].mean(),
        high_risk["Commute_Time"].mean()
    ]
})

high_risk_profile["Value"] = high_risk_profile["Value"].round(2)

print(high_risk_profile)

high_risk_profile.to_csv(
    "data/high_risk_profile.csv",
    index=False
)

# ============================================================
# 9. HIGH-RISK STUDENTS BY BRANCH
# ============================================================

print("\n9. HIGH-RISK STUDENTS BY BRANCH")
print("-" * 50)

high_risk_branch = (
    df[df["Risk_Level"] == "High Risk"]
    .groupby("Branch")
    .size()
    .reset_index(name="High_Risk_Students")
)

branch_total = (
    df.groupby("Branch")
    .size()
    .reset_index(name="Total_Students")
)

high_risk_branch = high_risk_branch.merge(
    branch_total,
    on="Branch",
    how="right"
)

high_risk_branch["High_Risk_Students"] = (
    high_risk_branch["High_Risk_Students"]
    .fillna(0)
    .astype(int)
)

high_risk_branch["High_Risk_Percentage"] = (
    high_risk_branch["High_Risk_Students"]
    / high_risk_branch["Total_Students"]
    * 100
).round(2)

high_risk_branch = high_risk_branch.sort_values(
    "High_Risk_Percentage",
    ascending=False
)

print(high_risk_branch)

high_risk_branch.to_csv(
    "data/high_risk_by_branch.csv",
    index=False
)

# ============================================================
# 10. POTENTIAL INTERVENTION GROUPS
# ============================================================

print("\n10. POTENTIAL INTERVENTION GROUPS")
print("-" * 50)

df["Support_Group"] = np.select(
    [
        df["Attendance"] < 60,
        df["Backlogs"] >= 2,
        df["LMS_Activity"] < 40,
        df["Study_Hours"] < 2,
        df["Risk_Level"] == "High Risk"
    ],
    [
        "Low Attendance",
        "Multiple Backlogs",
        "Low LMS Engagement",
        "Low Study Hours",
        "High Academic Risk"
    ],
    default="No Immediate Flag"
)

intervention_groups = (
    df.groupby("Support_Group")
    .agg(
        Students=("Student_ID", "count"),
        Average_CGPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance", "mean"),
        Average_LMS_Activity=("LMS_Activity", "mean")
    )
    .round(2)
    .sort_values("Students", ascending=False)
)

print(intervention_groups)

intervention_groups.to_csv(
    "data/intervention_groups.csv"
)

# ============================================================
# 11. KEY BUSINESS INSIGHTS
# ============================================================

print("\n11. KEY BUSINESS INSIGHTS")
print("-" * 50)

highest_attendance_group = attendance_groups["Average_CGPA"].idxmax()
lowest_attendance_group = attendance_groups["Average_CGPA"].idxmin()
highest_branch = branch_insights["Average_CGPA"].idxmax()
highest_lms_group = lms_insights["Average_CGPA"].idxmax()

print(
    f"1. '{highest_attendance_group}' has the highest "
    f"average CGPA among attendance groups."
)

print(
    f"2. '{lowest_attendance_group}' has the lowest "
    f"average CGPA among attendance groups."
)

print(
    f"3. '{highest_branch}' has the highest "
    f"average CGPA among branches."
)

print(
    f"4. '{highest_lms_group}' has the highest "
    f"average CGPA among LMS engagement groups."
)

print(
    f"5. {len(high_risk)} students are classified as High Risk."
)

# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS INSIGHTS ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated files:")
print("1. data/attendance_insights.csv")
print("2. data/backlog_insights.csv")
print("3. data/branch_insights.csv")
print("4. data/engagement_correlation.csv")
print("5. data/lms_insights.csv")
print("6. data/high_risk_profile.csv")
print("7. data/high_risk_by_branch.csv")
print("8. data/intervention_groups.csv")

print("\nNext stage: Predictive Analytics / Machine Learning")