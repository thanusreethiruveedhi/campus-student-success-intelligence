import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("data/student_success_data.csv")

print("=" * 60)
print("CAMPUS STUDENT SUCCESS INTELLIGENCE")
print("=" * 60)

# -----------------------------
# 1. BASIC DATA UNDERSTANDING
# -----------------------------

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Records:")
print(df.head())

# -----------------------------
# 2. MISSING VALUES
# -----------------------------

print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------------
# 3. DUPLICATE RECORDS
# -----------------------------

print("\nDuplicate Records:")
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# -----------------------------
# 4. CHECK UNIQUE STUDENT IDs
# -----------------------------

print("\nUnique Student IDs:")
print(df["Student_ID"].nunique())

# -----------------------------
# 5. NUMERICAL SUMMARY
# -----------------------------

print("\nNumerical Summary:")
print(df.describe())

# -----------------------------
# 6. CATEGORICAL SUMMARY
# -----------------------------

print("\nBranch Distribution:")
print(df["Branch"].value_counts())

print("\nYear Distribution:")
print(df["Year"].value_counts())

print("\nGender Distribution:")
print(df["Gender"].value_counts())

print("\nAcademic Status:")
print(df["Academic_Status"].value_counts())

print("\nRisk Level:")
print(df["Risk_Level"].value_counts())

# -----------------------------
# 7. DATA VALIDATION
# -----------------------------

print("\nData Validation:")

print(
    "Attendance outside 0-100:",
    ((df["Attendance"] < 0) | (df["Attendance"] > 100)).sum()
)

print(
    "CGPA outside 0-10:",
    ((df["Previous_CGPA"] < 0) | (df["Previous_CGPA"] > 10)).sum()
)

print(
    "Final CGPA outside 0-10:",
    ((df["Final_CGPA"] < 0) | (df["Final_CGPA"] > 10)).sum()
)

print(
    "Negative Backlogs:",
    (df["Backlogs"] < 0).sum()
)

# -----------------------------
# 8. SAVE CLEAN DATA
# -----------------------------

df.to_csv("data/student_success_clean.csv", index=False)

print("\nClean dataset saved successfully!")
print("Location: data/student_success_clean.csv")