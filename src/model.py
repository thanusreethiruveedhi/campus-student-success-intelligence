import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

print("=" * 70)
print("PREDICTIVE ANALYTICS - STUDENT RISK PREDICTION")
print("=" * 70)

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/student_success_clean.csv")

print("\n1. DATA LOADED")
print("-" * 50)

print(f"Students: {len(df)}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# 2. SELECT FEATURES
# ============================================================
#
# IMPORTANT:
# We do NOT use:
# Final_CGPA
# Academic_Status
# Risk_Level
#
# These are outcome-related fields and could cause data leakage.
# ============================================================

features = [
    "Attendance",
    "Previous_CGPA",
    "Internal_Marks",
    "Assignment_Score",
    "Study_Hours",
    "LMS_Activity",
    "Library_Visits",
    "Lab_Usage",
    "Certifications",
    "Projects",
    "Hackathons",
    "Internships",
    "Commute_Time",
    "Backlogs"
]

target = "Risk_Level"

X = df[features]
y = df[target]

print("\n2. FEATURES SELECTED")
print("-" * 50)

for feature in features:
    print("-", feature)

print(f"\nTarget: {target}")

# ============================================================
# 3. CHECK TARGET DISTRIBUTION
# ============================================================

print("\n3. TARGET DISTRIBUTION")
print("-" * 50)

print(y.value_counts())

# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

print("\n4. TRAIN / TEST SPLIT")
print("-" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training records: {len(X_train)}")
print(f"Testing records : {len(X_test)}")

# ============================================================
# 5. CREATE RANDOM FOREST MODEL
# ============================================================

print("\n5. TRAINING RANDOM FOREST MODEL")
print("-" * 50)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model training completed.")

# ============================================================
# 6. MAKE PREDICTIONS
# ============================================================

print("\n6. MAKING PREDICTIONS")
print("-" * 50)

y_pred = model.predict(X_test)

print("Predictions completed.")

# ============================================================
# 7. MODEL PERFORMANCE
# ============================================================

print("\n7. MODEL PERFORMANCE")
print("-" * 50)

accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(
    y_test,
    y_pred,
    average="macro"
)

print(f"Accuracy : {accuracy:.4f}")
print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Macro F1 : {macro_f1:.4f}")

# ============================================================
# 8. CLASSIFICATION REPORT
# ============================================================

print("\n8. CLASSIFICATION REPORT")
print("-" * 50)

report = classification_report(
    y_test,
    y_pred,
    zero_division=0
)

print(report)

# Save classification report
report_dict = classification_report(
    y_test,
    y_pred,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report_dict).transpose()

report_df.to_csv(
    "data/model_classification_report.csv"
)

# ============================================================
# 9. CONFUSION MATRIX
# ============================================================

print("\n9. CONFUSION MATRIX")
print("-" * 50)

class_order = [
    "Low Risk",
    "Medium Risk",
    "High Risk"
]

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=class_order
)

cm_df = pd.DataFrame(
    cm,
    index=class_order,
    columns=class_order
)

print(cm_df)

cm_df.to_csv(
    "data/confusion_matrix.csv"
)

# ============================================================
# 10. FEATURE IMPORTANCE
# ============================================================

print("\n10. FEATURE IMPORTANCE")
print("-" * 50)

feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    "Importance",
    ascending=False
)

feature_importance["Importance"] = (
    feature_importance["Importance"].round(4)
)

print(feature_importance)

feature_importance.to_csv(
    "data/feature_importance.csv",
    index=False
)

# ============================================================
# 11. SAVE MODEL
# ============================================================

print("\n11. SAVING MODEL")
print("-" * 50)

with open(
    "data/student_risk_model.pkl",
    "wb"
) as file:

    pickle.dump(model, file)

print("Model saved to:")
print("data/student_risk_model.pkl")

# ============================================================
# 12. SAVE TEST PREDICTIONS
# ============================================================

print("\n12. SAVING TEST PREDICTIONS")
print("-" * 50)

prediction_results = X_test.copy()

prediction_results["Actual_Risk"] = y_test.values
prediction_results["Predicted_Risk"] = y_pred

prediction_results.to_csv(
    "data/test_predictions.csv",
    index=False
)

print("Predictions saved to:")
print("data/test_predictions.csv")

# ============================================================
# 13. SAMPLE PREDICTIONS
# ============================================================

print("\n13. SAMPLE PREDICTIONS")
print("-" * 50)

sample_results = prediction_results[
    [
        "Attendance",
        "Previous_CGPA",
        "Backlogs",
        "Actual_Risk",
        "Predicted_Risk"
    ]
].head(10)

print(sample_results.to_string(index=False))

# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("PREDICTIVE ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"\nFinal Model Accuracy: {accuracy * 100:.2f}%")
print(f"Macro F1 Score      : {macro_f1:.4f}")

print("\nGenerated files:")
print("1. data/model_classification_report.csv")
print("2. data/confusion_matrix.csv")
print("3. data/feature_importance.csv")
print("4. data/student_risk_model.pkl")
print("5. data/test_predictions.csv")

print("\nNext stage: Interactive Streamlit BI Dashboard")