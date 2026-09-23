# 🎓 Campus Resource & Student Success Intelligence System

## 📌 Project Overview

The **Campus Resource & Student Success Intelligence System** is a Business Intelligence and Predictive Analytics project designed to analyze student academic performance, learning engagement, campus resource usage, and academic risk.

The project combines:

- Python
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Streamlit
- Exploratory Data Analysis
- Predictive Analytics
- Interactive Business Intelligence dashboards

The system transforms student-level data into meaningful insights and provides a prototype model for classifying students into **Low Risk, Medium Risk, and High Risk** categories.

> **Important:** The dataset used in this project is synthetic and created for academic demonstration. Model results should not be interpreted as validated real-world student-risk predictions.


---

# 🎯 Problem Statement

Educational institutions generate large amounts of student information related to academics, attendance, learning platforms, assignments, campus resources, projects, certifications, internships, and other activities.

However, raw student data alone does not easily reveal:

- Which factors are associated with academic performance
- How attendance relates to CGPA
- How student engagement varies
- Which groups require additional academic attention
- Which factors contribute to the model's prediction of academic risk

This project converts these data points into an interactive Business Intelligence system.


---

# 🎯 Objectives

The major objectives are:

1. Analyze student academic performance.
2. Study attendance and its association with Final CGPA.
3. Analyze LMS, library, laboratory, and other engagement activities.
4. Identify patterns associated with academic performance.
5. Analyze student risk categories.
6. Identify groups that may require academic support.
7. Build a machine-learning prototype for student risk classification.
8. Evaluate the predictive model using classification metrics.
9. Develop an interactive Streamlit dashboard.
10. Present data-driven insights through visualizations and KPIs.


---

# ❓ Business Questions

## Academic Performance

- What is the average Final CGPA?
- How does performance vary across branches?
- How is attendance associated with Final CGPA?
- How is Previous CGPA related to Final CGPA?
- How are backlogs associated with academic performance?
- How do assignment and internal marks relate to Final CGPA?

## Student Engagement

- What is the average LMS activity?
- How frequently do students use the library?
- How much laboratory activity is recorded?
- What is the average number of projects?
- How many certifications do students have?
- How are engagement variables associated with Final CGPA?

## Academic Risk

- How many students are classified as High Risk?
- How is risk distributed across branches?
- What characteristics are common among High-Risk students?
- How are backlogs and attendance represented among different risk groups?
- How accurately can the prototype model classify student risk?

## Institutional Intelligence

- Which student characteristics are associated with academic success?
- Which groups may require additional academic support?
- Which engagement areas can be monitored?
- How can BI dashboards support data-driven academic monitoring?


---

# 📊 Dataset

The project uses a **synthetic dataset containing 1,000 students**.

The dataset contains **21 columns**.

### Main Dimensions

| Category | Variables |
|---|---|
| Student Information | Student_ID, Branch, Year, Gender |
| Academic | Previous_CGPA, Internal_Marks, Assignment_Score, Final_CGPA |
| Attendance | Attendance |
| Learning | Study_Hours, LMS_Activity |
| Campus Resources | Library_Visits, Lab_Usage |
| Skill Development | Certifications, Projects, Hackathons, Internships |
| Other Factors | Commute_Time, Backlogs |
| Classification | Academic_Status, Risk_Level |


---

# 🧹 Data Preparation

The project performs the following data-quality checks:

- Missing-value detection
- Duplicate-record detection
- Duplicate Student ID detection
- Numeric range validation
- Data cleaning
- Feature preparation
- Dataset export

The cleaned dataset is saved as:

```text
data/student_success_clean.csv 
🔎 Exploratory Data Analysis

The EDA stage examines:

Student distribution
Academic performance
Attendance
Branch performance
Academic status
Risk distribution
Backlogs
Campus-resource usage
Correlations with Final CGPA
High-risk student profiles

The analysis generates reusable CSV and HTML outputs inside the data/ directory.

💡 Key Business Insights

Based on the current synthetic dataset:

Academic Performance

The average Final CGPA is approximately:

7.33

The average Previous CGPA is approximately:

7.51

The average change from Previous CGPA to Final CGPA is approximately:

-0.18
Attendance

The average CGPA varies across attendance groups.

Attendance Group	Students	Average CGPA
Below 60%	17	6.64
60–75%	282	7.15
75–85%	393	7.32
Above 85%	308	7.53

This shows an association between attendance group and average CGPA within this synthetic dataset.

Risk Distribution

The dataset contains:

Risk Level	Students
Low Risk	650
Medium Risk	230
High Risk	120

The prototype dataset therefore contains 120 High-Risk students.

High-Risk Student Profile

The High-Risk group has approximately:

Average Attendance: 76.79%
Average Previous CGPA: 6.34
Average Final CGPA: 6.49
Average Internal Marks: 69.20
Average Assignment Score: 72.91
Average LMS Activity: 64.54
Average Study Hours: 4.15
Average Backlogs: 1.46
Correlation with Final CGPA
Factor	Correlation
Previous CGPA	0.716
Internal Marks	0.286
Attendance	0.276
LMS Activity	0.260
Assignment Score	0.186
Study Hours	0.166
Projects	0.127
Certifications	0.036
Lab Usage	0.015
Internships	0.014
Hackathons	0.010
Library Visits	0.000
Commute Time	-0.093
Backlogs	-0.401

Correlation describes association and does not establish causation.

🤖 Predictive Analytics

A Random Forest Classifier is used to classify students into:

Low Risk
Medium Risk
High Risk
Features Used

The model uses:

Attendance
Previous_CGPA
Internal_Marks
Assignment_Score
Study_Hours
LMS_Activity
Library_Visits
Lab_Usage
Certifications
Projects
Hackathons
Internships
Commute_Time
Backlogs

Final_CGPA, Academic_Status, and Risk_Level are excluded from the model features to avoid target leakage.

📈 Model Performance

The model was evaluated on a 200-student test set.

Overall Metrics
Metric	Result
Accuracy	88.50%
Macro F1 Score	84.36%
Classification Performance
Risk Category	Precision	Recall	F1 Score
High Risk	0.778	0.875	0.824
Low Risk	0.975	0.915	0.944
Medium Risk	0.725	0.804	0.763

The confusion matrix and detailed model results are available in:

data/confusion_matrix.csv
data/model_classification_report.csv
🔍 Feature Importance

The Random Forest model identified the following features as the most influential within this prototype:

Previous_CGPA
Backlogs
Attendance
Study_Hours
Internal_Marks
LMS_Activity
Commute_Time
Assignment_Score
Lab_Usage
Library_Visits
Projects
Hackathons
Certifications
Internships

Feature importance indicates contribution to the model's decision process; it does not establish causal relationships.

📊 Interactive Dashboard

The Streamlit dashboard contains four major sections.

1. Executive Overview

Provides:

Total students
Average Final CGPA
Average attendance
High-risk student count
Academic-status distribution
Risk distribution
Branch performance
Key insights
2. Academic Intelligence

Provides:

Previous CGPA
Final CGPA
Average backlogs
Attendance vs Final CGPA
Attendance-group analysis
Backlogs vs CGPA
Branch-wise CGPA
3. Student Engagement

Provides:

LMS activity
Library visits
Lab usage
Study hours
LMS activity vs CGPA
Resource usage
Correlation analysis
4. Risk & Prediction

Provides:

Low/Medium/High Risk counts
High-risk percentage by branch
Model accuracy
Macro F1 score
Classification report
Confusion matrix
Feature importance
Individual student risk prediction
Prediction probabilities
🏗️ Project Architecture
Raw Synthetic Data
        ↓
Data Cleaning & Validation
        ↓
Exploratory Data Analysis
        ↓
Business Question Analysis
        ↓
Insight Generation
        ↓
Predictive Analytics
        ↓
Student Risk Classification
        ↓
Model Evaluation
        ↓
Interactive Streamlit Dashboard
        ↓
Data-Driven Recommendations
📁 Project Structure
campus-student-success-intelligence/
│
├── data/
│   ├── student_success_data.csv
│   ├── student_success_clean.csv
│   ├── data_dictionary.csv
│   ├── model_classification_report.csv
│   ├── confusion_matrix.csv
│   ├── feature_importance.csv
│   ├── test_predictions.csv
│   └── analysis outputs
│
├── src/
│   ├── generate_data.py
│   ├── analysis.py
│   ├── insights.py
│   └── model.py
│
├── app.py
├── requirements.txt
└── README.md
🛠️ Technology Stack
Technology	Purpose
Python	Core programming
Pandas	Data manipulation
NumPy	Numerical operations
Plotly	Interactive visualizations
Scikit-learn	Machine learning
Streamlit	Interactive dashboard
Statsmodels	Statistical trendline support
GitHub	Version control and project hosting
GitHub Codespaces	Cloud development environment
▶️ How to Run
1. Clone the repository
git clone <your-github-repository-url>
2. Open the project
cd campus-student-success-intelligence
3. Install dependencies
pip install -r requirements.txt
4. Generate the dataset
python src/generate_data.py
5. Run analysis
python src/analysis.py
6. Generate business insights
python src/insights.py
7. Train the prediction model
python src/model.py
8. Start the Streamlit dashboard
python -m streamlit run app.py
GitHub Codespaces

If using the .venv environment created for this project, use:

./.venv/bin/python -m streamlit run app.py
⚠️ Limitations

This project has several limitations:

The dataset is synthetic.
The relationships in the generated data are designed for project demonstration.
The model has not been validated on real institutional data.
Model performance on synthetic data does not represent expected performance on real students.
Correlation and feature importance do not establish causation.
A real deployment would require appropriate privacy, governance, consent, and institutional review.
🚀 Future Scope

Possible future improvements include:

Use anonymized real institutional data.
Add semester-wise student tracking.
Add historical academic trends.
Add real LMS activity data.
Add automated intervention tracking.
Add faculty-level dashboards.
Add department-level dashboards.
Add model monitoring.
Compare multiple classification algorithms.
Add explainable AI techniques.
Integrate the dashboard with institutional databases.
Add role-based dashboard access.
📌 Conclusion

The Campus Resource & Student Success Intelligence System demonstrates how Business Intelligence and Predictive Analytics can be combined to transform student-related data into useful analytical insights.

The project follows an end-to-end workflow:

Data → Cleaning → EDA → Business Questions → Insights → Machine Learning → Dashboard

The resulting dashboard provides an interactive way to explore academic performance, engagement patterns, risk categories, and predictive-model results.

The current implementation is an academic prototype using synthetic data and provides a foundation that could be extended with appropriately governed real-world institutional data.

👩‍💻 Author

Thanusree

B.Tech — CSE with AI Specialization