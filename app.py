import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Campus Student Success Intelligence",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/student_success_clean.csv")


@st.cache_resource
def load_model():
    with open("data/student_risk_model.pkl", "rb") as file:
        return pickle.load(file)


@st.cache_data
def load_classification_report():
    return pd.read_csv("data/model_classification_report.csv")


@st.cache_data
def load_confusion_matrix():
    return pd.read_csv("data/confusion_matrix.csv")


df = load_data()
model = load_model()
classification_report = load_classification_report()
confusion_matrix_df = load_confusion_matrix()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎓 Student Success BI")

st.sidebar.markdown(
    """
    ### Navigation

    Explore the student intelligence system:

    - Executive Overview
    - Academic Intelligence
    - Student Engagement
    - Risk & Prediction
    """
)

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Overview",
        "Academic Intelligence",
        "Student Engagement",
        "Risk & Prediction"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "This dashboard uses synthetic student data created "
    "for an academic Business Intelligence project."
)


# ============================================================
# COMMON FILTERS
# ============================================================

st.sidebar.markdown("### Filters")

branch_filter = st.sidebar.multiselect(
    "Branch",
    options=sorted(df["Branch"].unique()),
    default=sorted(df["Branch"].unique())
)

year_filter = st.sidebar.multiselect(
    "Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

status_filter = st.sidebar.multiselect(
    "Academic Status",
    options=sorted(df["Academic_Status"].unique()),
    default=sorted(df["Academic_Status"].unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=["Low Risk", "Medium Risk", "High Risk"],
    default=["Low Risk", "Medium Risk", "High Risk"]
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Branch"].isin(branch_filter)) &
    (df["Year"].isin(year_filter)) &
    (df["Academic_Status"].isin(status_filter)) &
    (df["Risk_Level"].isin(risk_filter)) &
    (df["Gender"].isin(gender_filter))
].copy()


# ============================================================
# NO DATA WARNING
# ============================================================

if len(filtered_df) == 0:

    st.warning(
        "No students match the selected filters. "
        "Please change the filters from the sidebar."
    )

    st.stop()


# ============================================================
# PAGE 1 - EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="main-title">'
        '🎓 Campus Resource & Student Success Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Executive overview of academic performance, student engagement '
        'and academic risk'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    total_students = len(filtered_df)

    avg_cgpa = filtered_df["Final_CGPA"].mean()

    avg_attendance = filtered_df["Attendance"].mean()

    high_risk = (
        filtered_df["Risk_Level"] == "High Risk"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Students",
        f"{total_students:,}"
    )

    col2.metric(
        "Average Final CGPA",
        f"{avg_cgpa:.2f}"
    )

    col3.metric(
        "Average Attendance",
        f"{avg_attendance:.1f}%"
    )

    col4.metric(
        "High-Risk Students",
        f"{high_risk:,}"
    )


    st.markdown("---")


    # --------------------------------------------------------
    # DISTRIBUTIONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        status_counts = (
            filtered_df["Academic_Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Academic_Status",
            "Students"
        ]

        fig = px.pie(
            status_counts,
            names="Academic_Status",
            values="Students",
            hole=0.45,
            title="Academic Status Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        risk_counts = (
            filtered_df["Risk_Level"]
            .value_counts()
            .reindex(
                ["Low Risk", "Medium Risk", "High Risk"]
            )
            .fillna(0)
            .reset_index()
        )

        risk_counts.columns = [
            "Risk_Level",
            "Students"
        ]

        fig = px.bar(
            risk_counts,
            x="Risk_Level",
            y="Students",
            text="Students",
            title="Student Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BRANCH PERFORMANCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Branch Performance</div>',
        unsafe_allow_html=True
    )

    branch_summary = (
        filtered_df
        .groupby("Branch")
        .agg(
            Students=("Student_ID", "count"),
            Average_CGPA=("Final_CGPA", "mean"),
            Average_Attendance=("Attendance", "mean"),
            High_Risk=(
                "Risk_Level",
                lambda x: (x == "High Risk").sum()
            )
        )
        .reset_index()
    )

    branch_summary["Average_CGPA"] = (
        branch_summary["Average_CGPA"].round(2)
    )

    branch_summary["Average_Attendance"] = (
        branch_summary["Average_Attendance"].round(2)
    )

    st.dataframe(
        branch_summary,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '💡 Key Insights & Recommended Actions'
        '</div>',
        unsafe_allow_html=True
    )

    insight_col1, insight_col2 = st.columns(2)


    with insight_col1:

        # Attendance insight

        insight_df = filtered_df.copy()

        insight_df["Attendance_Group"] = pd.cut(
            insight_df["Attendance"],
            bins=[0, 60, 75, 85, 100],
            labels=[
                "Below 60%",
                "60-75%",
                "75-85%",
                "Above 85%"
            ],
            include_lowest=True
        )

        attendance_insight = (
            insight_df
            .groupby(
                "Attendance_Group",
                observed=True
            )["Final_CGPA"]
            .mean()
        )

        highest_attendance_group = (
            attendance_insight.idxmax()
        )

        lowest_attendance_group = (
            attendance_insight.idxmin()
        )

        st.info(
            f"📌 **Attendance Insight**\n\n"
            f"{highest_attendance_group} has the highest average "
            f"CGPA ({attendance_insight.max():.2f}), while "
            f"{lowest_attendance_group} has the lowest "
            f"({attendance_insight.min():.2f})."
        )


        # Branch insight

        branch_cgpa = (
            filtered_df
            .groupby("Branch")["Final_CGPA"]
            .mean()
        )

        top_branch = branch_cgpa.idxmax()

        st.info(
            f"🏫 **Branch Insight**\n\n"
            f"{top_branch} has the highest average CGPA "
            f"among the currently selected branches "
            f"({branch_cgpa.max():.2f})."
        )


    with insight_col2:

        # Risk insight

        high_risk_percentage = (
            high_risk / total_students * 100
        )

        st.warning(
            f"⚠️ **Risk Insight**\n\n"
            f"{high_risk:,} students are classified as "
            f"High Risk, representing "
            f"{high_risk_percentage:.1f}% of the selected students."
        )


        # Backlog insight

        backlog_students = (
            filtered_df["Backlogs"] > 0
        ).sum()

        backlog_percentage = (
            backlog_students / total_students * 100
        )

        st.info(
            f"📚 **Backlog Insight**\n\n"
            f"{backlog_students:,} students have at least "
            f"one backlog ({backlog_percentage:.1f}% of "
            f"selected students)."
        )


    st.markdown("---")

    st.caption(
        "Note: These insights describe patterns in the synthetic "
        "dataset and should not be interpreted as causal relationships."
    )


# ============================================================
# PAGE 2 - ACADEMIC INTELLIGENCE
# ============================================================

elif page == "Academic Intelligence":

    st.markdown(
        '<div class="main-title">📚 Academic Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Explore factors associated with student academic performance'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Previous CGPA",
        f"{filtered_df['Previous_CGPA'].mean():.2f}"
    )

    col2.metric(
        "Average Final CGPA",
        f"{filtered_df['Final_CGPA'].mean():.2f}"
    )

    col3.metric(
        "Average Backlogs",
        f"{filtered_df['Backlogs'].mean():.2f}"
    )


    st.markdown("---")


    # --------------------------------------------------------
    # ATTENDANCE VS CGPA
    # --------------------------------------------------------

    st.markdown("### Attendance vs Final CGPA")

    fig = px.scatter(
        filtered_df,
        x="Attendance",
        y="Final_CGPA",
        color="Risk_Level",
        hover_data=[
            "Student_ID",
            "Branch",
            "Year"
        ],
        title="Attendance and Academic Performance",
        trendline="ols"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # ATTENDANCE GROUP
    # --------------------------------------------------------

    academic_df = filtered_df.copy()

    academic_df["Attendance_Group"] = pd.cut(
        academic_df["Attendance"],
        bins=[0, 60, 75, 85, 100],
        labels=[
            "Below 60%",
            "60-75%",
            "75-85%",
            "Above 85%"
        ],
        include_lowest=True
    )

    attendance_summary = (
        academic_df
        .groupby(
            "Attendance_Group",
            observed=True
        )
        .agg(
            Students=("Student_ID", "count"),
            Average_CGPA=("Final_CGPA", "mean")
        )
        .reset_index()
    )

    attendance_summary["Average_CGPA"] = (
        attendance_summary["Average_CGPA"].round(2)
    )

    fig = px.bar(
        attendance_summary,
        x="Attendance_Group",
        y="Average_CGPA",
        text="Average_CGPA",
        title="Average CGPA by Attendance Group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # BACKLOGS AND BRANCH
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        backlog_summary = (
            filtered_df
            .groupby("Backlogs")
            .agg(
                Students=("Student_ID", "count"),
                Average_CGPA=("Final_CGPA", "mean")
            )
            .reset_index()
        )

        fig = px.bar(
            backlog_summary,
            x="Backlogs",
            y="Average_CGPA",
            text="Average_CGPA",
            title="Backlogs vs Average CGPA"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        branch_cgpa = (
            filtered_df
            .groupby("Branch")["Final_CGPA"]
            .mean()
            .reset_index()
        )

        branch_cgpa["Final_CGPA"] = (
            branch_cgpa["Final_CGPA"].round(2)
        )

        fig = px.bar(
            branch_cgpa,
            x="Branch",
            y="Final_CGPA",
            text="Final_CGPA",
            title="Average CGPA by Branch"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # ACADEMIC OBSERVATION
    # --------------------------------------------------------

    st.markdown("---")

    st.info(
        "📌 **Interpretation:** Attendance and previous academic "
        "performance show measurable associations with Final CGPA "
        "in this synthetic dataset. Association does not establish causation."
    )


# ============================================================
# PAGE 3 - STUDENT ENGAGEMENT
# ============================================================

elif page == "Student Engagement":

    st.markdown(
        '<div class="main-title">'
        '📊 Student Engagement Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Analyze learning activity and campus resource engagement'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ENGAGEMENT KPIs
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "LMS Activity",
        f"{filtered_df['LMS_Activity'].mean():.1f}"
    )

    col2.metric(
        "Library Visits",
        f"{filtered_df['Library_Visits'].mean():.1f}"
    )

    col3.metric(
        "Lab Usage",
        f"{filtered_df['Lab_Usage'].mean():.1f}"
    )

    col4.metric(
        "Study Hours",
        f"{filtered_df['Study_Hours'].mean():.1f}"
    )


    st.markdown("---")


    # --------------------------------------------------------
    # LMS VS CGPA
    # --------------------------------------------------------

    fig = px.scatter(
        filtered_df,
        x="LMS_Activity",
        y="Final_CGPA",
        color="Risk_Level",
        hover_data=[
            "Student_ID",
            "Branch",
            "Year"
        ],
        title="LMS Activity vs Final CGPA",
        trendline="ols"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # RESOURCE USAGE
    # --------------------------------------------------------

    resource_data = pd.DataFrame({
        "Resource": [
            "LMS Activity",
            "Lab Usage",
            "Library Visits",
            "Projects",
            "Certifications",
            "Hackathons",
            "Internships"
        ],
        "Average Usage": [
            filtered_df["LMS_Activity"].mean(),
            filtered_df["Lab_Usage"].mean(),
            filtered_df["Library_Visits"].mean(),
            filtered_df["Projects"].mean(),
            filtered_df["Certifications"].mean(),
            filtered_df["Hackathons"].mean(),
            filtered_df["Internships"].mean()
        ]
    })

    fig = px.bar(
        resource_data,
        x="Resource",
        y="Average Usage",
        title="Average Student Engagement by Resource",
        text="Average Usage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CORRELATION
    # --------------------------------------------------------

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

    correlation = (
        filtered_df[
            engagement_columns + ["Final_CGPA"]
        ]
        .corr()["Final_CGPA"]
        .drop("Final_CGPA")
        .sort_values(ascending=False)
        .reset_index()
    )

    correlation.columns = [
        "Factor",
        "Correlation"
    ]

    fig = px.bar(
        correlation,
        x="Correlation",
        y="Factor",
        orientation="h",
        title="Factors Associated with Final CGPA",
        text="Correlation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.info(
        "📌 **Interpretation:** Correlation indicates the direction "
        "and strength of association in the dataset. It does not "
        "prove that one factor causes changes in CGPA."
    )


# ============================================================
# PAGE 4 - RISK & PREDICTION
# ============================================================

elif page == "Risk & Prediction":

    st.markdown(
        '<div class="main-title">'
        '⚠️ Risk & Prediction Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Analyze risk patterns and evaluate the student-risk '
        'prediction prototype'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # RISK KPIs
    # --------------------------------------------------------

    high_risk_count = (
        filtered_df["Risk_Level"] == "High Risk"
    ).sum()

    medium_risk_count = (
        filtered_df["Risk_Level"] == "Medium Risk"
    ).sum()

    low_risk_count = (
        filtered_df["Risk_Level"] == "Low Risk"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Low Risk",
        f"{low_risk_count:,}"
    )

    col2.metric(
        "Medium Risk",
        f"{medium_risk_count:,}"
    )

    col3.metric(
        "High Risk",
        f"{high_risk_count:,}"
    )


    st.markdown("---")


    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    st.markdown("## 🤖 Predictive Model Performance")

    st.info(
        "The Random Forest model was trained to classify students "
        "into Low Risk, Medium Risk and High Risk categories. "
        "The reported metrics are based on the 200-student test set "
        "from this synthetic dataset."
    )


    # --------------------------------------------------------
    # LOAD ACCURACY AND F1
    # --------------------------------------------------------

    accuracy_row = classification_report[
        classification_report["Unnamed: 0"] == "accuracy"
    ]

    macro_row = classification_report[
        classification_report["Unnamed: 0"] == "macro avg"
    ]


    if len(accuracy_row) > 0:

        accuracy = float(
            accuracy_row["precision"].iloc[0]
        )

    else:

        accuracy = 0


    if len(macro_row) > 0:

        macro_f1 = float(
            macro_row["f1-score"].iloc[0]
        )

    else:

        macro_f1 = 0


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Model Accuracy",
        f"{accuracy * 100:.2f}%"
    )

    col2.metric(
        "Macro F1 Score",
        f"{macro_f1 * 100:.2f}%"
    )

    col3.metric(
        "Test Students",
        "200"
    )


    # --------------------------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------------------------

    st.markdown("### 📋 Classification Report")

    report_display = classification_report.copy()

    report_display = report_display.rename(
        columns={
            "Unnamed: 0": "Risk Category",
            "f1-score": "F1 Score"
        }
    )

    report_display = report_display[
        [
            "Risk Category",
            "precision",
            "recall",
            "F1 Score",
            "support"
        ]
    ]

    report_display["precision"] = (
        report_display["precision"].round(3)
    )

    report_display["recall"] = (
        report_display["recall"].round(3)
    )

    report_display["F1 Score"] = (
        report_display["F1 Score"].round(3)
    )

    st.dataframe(
        report_display,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    st.markdown("### 🧩 Confusion Matrix")

    cm = confusion_matrix_df.copy()

    cm = cm.rename(
        columns={
            "Unnamed: 0": "Actual Risk"
        }
    )

    st.dataframe(
        cm,
        use_container_width=True,
        hide_index=True
    )


    # Heatmap version

    cm_matrix = confusion_matrix_df.copy()

    cm_matrix = cm_matrix.set_index("Unnamed: 0")

    cm_matrix.index.name = "Actual"

    cm_matrix.columns.name = "Predicted"

    fig = px.imshow(
        cm_matrix,
        text_auto=True,
        title="Risk Prediction Confusion Matrix",
        labels={
            "x": "Predicted Risk",
            "y": "Actual Risk",
            "color": "Students"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # MODEL PERFORMANCE EXPLANATION
    # --------------------------------------------------------

    performance_col1, performance_col2 = st.columns(2)


    with performance_col1:

        st.markdown("### What the metrics mean")

        st.write(
            """
            **Accuracy** shows the proportion of test students
            whose risk category was predicted correctly.

            **Precision** shows how often predictions for a
            particular risk category were correct.

            **Recall** shows how many students belonging to a
            particular risk category were successfully identified.

            **F1 Score** balances precision and recall.
            """
        )


    with performance_col2:

        st.markdown("### Model Observation")

        st.write(
            """
            The model performs differently across the three
            risk categories. The Low Risk class has the strongest
            F1 score, while Medium Risk is more difficult to
            classify accurately.

            Because the dataset is synthetic and the target risk
            categories were generated from related variables,
            these results should be treated as a prototype
            demonstration rather than real-world validation.
            """
        )


    st.markdown("---")


    # ========================================================
    # HIGH-RISK STUDENTS BY BRANCH
    # ========================================================

    st.markdown("### High-Risk Students by Branch")

    risk_branch = (
        filtered_df
        .groupby("Branch")
        .agg(
            Total_Students=("Student_ID", "count"),
            High_Risk_Students=(
                "Risk_Level",
                lambda x: (x == "High Risk").sum()
            )
        )
        .reset_index()
    )

    risk_branch["High_Risk_Percentage"] = (
        risk_branch["High_Risk_Students"]
        / risk_branch["Total_Students"]
        * 100
    ).round(2)

    fig = px.bar(
        risk_branch,
        x="Branch",
        y="High_Risk_Percentage",
        text="High_Risk_Percentage",
        title="High-Risk Student Percentage by Branch"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    st.markdown("### 🔍 Model Feature Importance")

    feature_importance = pd.DataFrame({
        "Feature": model.feature_names_in_,
        "Importance": model.feature_importances_
    })

    feature_importance = (
        feature_importance
        .sort_values(
            "Importance",
            ascending=True
        )
    )

    fig = px.bar(
        feature_importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Factors Used by the Risk Prediction Model",
        text="Importance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.info(
        "Feature importance indicates how much each feature "
        "contributed to the Random Forest's decision process. "
        "It should not be interpreted as proof of causation."
    )


    # ========================================================
    # INDIVIDUAL STUDENT PREDICTION
    # ========================================================

    st.markdown("---")

    st.markdown(
        "### 🔮 Individual Student Risk Prediction"
    )

    st.write(
        "Enter student information to generate a predicted "
        "risk category and probability distribution."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=80.0
        )

        previous_cgpa = st.number_input(
            "Previous CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.5
        )

        internal_marks = st.number_input(
            "Internal Marks",
            min_value=0.0,
            max_value=100.0,
            value=72.0
        )

        assignment_score = st.number_input(
            "Assignment Score",
            min_value=0.0,
            max_value=100.0,
            value=74.0
        )

        study_hours = st.number_input(
            "Study Hours per Day",
            min_value=0.0,
            max_value=15.0,
            value=4.5
        )


    with col2:

        lms_activity = st.number_input(
            "LMS Activity",
            min_value=0.0,
            max_value=100.0,
            value=68.0
        )

        library_visits = st.number_input(
            "Library Visits",
            min_value=0,
            max_value=30,
            value=5
        )

        lab_usage = st.number_input(
            "Lab Usage",
            min_value=0.0,
            max_value=100.0,
            value=70.0
        )

        certifications = st.number_input(
            "Certifications",
            min_value=0,
            max_value=20,
            value=2
        )

        projects = st.number_input(
            "Projects",
            min_value=0,
            max_value=20,
            value=2
        )


    with col3:

        hackathons = st.number_input(
            "Hackathons",
            min_value=0,
            max_value=20,
            value=1
        )

        internships = st.number_input(
            "Internships",
            min_value=0,
            max_value=10,
            value=1
        )

        commute_time = st.number_input(
            "Commute Time (minutes)",
            min_value=0.0,
            max_value=200.0,
            value=40.0
        )

        backlogs = st.number_input(
            "Backlogs",
            min_value=0,
            max_value=10,
            value=0
        )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    if st.button(
        "🔮 Predict Student Risk",
        use_container_width=True
    ):

        input_data = pd.DataFrame({
            "Attendance": [attendance],
            "Previous_CGPA": [previous_cgpa],
            "Internal_Marks": [internal_marks],
            "Assignment_Score": [assignment_score],
            "Study_Hours": [study_hours],
            "LMS_Activity": [lms_activity],
            "Library_Visits": [library_visits],
            "Lab_Usage": [lab_usage],
            "Certifications": [certifications],
            "Projects": [projects],
            "Hackathons": [hackathons],
            "Internships": [internships],
            "Commute_Time": [commute_time],
            "Backlogs": [backlogs]
        })


        prediction = model.predict(
            input_data
        )[0]


        probabilities = model.predict_proba(
            input_data
        )[0]


        classes = model.classes_


        probability_df = pd.DataFrame({
            "Risk Level": classes,
            "Probability": probabilities
        })


        probability_df["Probability"] = (
            probability_df["Probability"] * 100
        ).round(2)


        st.markdown("### Prediction Result")


        if prediction == "High Risk":

            st.error(
                f"Predicted Student Risk: **{prediction}**"
            )

        elif prediction == "Medium Risk":

            st.warning(
                f"Predicted Student Risk: **{prediction}**"
            )

        else:

            st.success(
                f"Predicted Student Risk: **{prediction}**"
            )


        fig = px.bar(
            probability_df,
            x="Risk Level",
            y="Probability",
            text="Probability",
            title="Prediction Probability"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "Campus Resource & Student Success Intelligence System"
)

st.sidebar.caption(
    "Built with Python, Pandas, Plotly, Scikit-learn and Streamlit"
)