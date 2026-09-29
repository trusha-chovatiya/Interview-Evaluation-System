import streamlit as st
import pandas as pd

from database import (
    create_tables,
    initialize_default_students,
    get_students,
    add_student,
    update_student,
    delete_student,
    save_marks,
    delete_marks
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Interview Evaluation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

create_tables()
initialize_default_students()


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f5f7fb;
    font-family: 'Inter', sans-serif;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

section[data-testid="stSidebar"] * {
    color: white;
}

section[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* ================= HERO ================= */

.hero-box {
    background: linear-gradient(135deg, #0f172a, #1d4ed8);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin: 0 0 10px 0;
}

.hero-subtitle {
    font-size: 16px;
    margin: 0;
    color: #dbeafe;
}

/* ================= METRIC CARDS ================= */

.metric-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.06);
}

.metric-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.metric-number {
    color: #0f172a;
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}

/* ================= SECTION TITLE ================= */

.section-heading {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* ================= STUDENT CARD ================= */

.student-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
}

.student-name {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
}

/* ================= BUTTONS ================= */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

/* ================= INPUTS ================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 10px;
}

/* ================= FOOTER ================= */

.footer-box {
    text-align: center;
    padding: 25px;
    margin-top: 40px;
    color: #64748b;
    font-size: 13px;
}

/* ================= SCORE CARD ================= */

.score-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
}

.score-title {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.score-value {
    color: #2563eb;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

/* ================= TOP PERFORMER ================= */

.top-performer {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    margin-bottom: 25px;
}

.top-title {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.top-name {
    color: #0f172a;
    font-size: 30px;
    font-weight: 800;
    margin-top: 5px;
}

.top-score {
    color: #2563eb;
    font-size: 18px;
    font-weight: 700;
    margin-top: 5px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTION FOR HTML
# =========================================================

def show_html(html_code):
    """
    Render HTML using Streamlit's native HTML renderer.
    This avoids the Markdown code-block problem.
    """
    if hasattr(st, "html"):
        st.html(html_code)
    else:
        st.markdown(
            html_code,
            unsafe_allow_html=True
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    show_html("""
    <div style="
        text-align:center;
        padding:20px 5px 25px 5px;
    ">
        <div style="font-size:48px;">🎓</div>

        <div style="
            font-size:23px;
            font-weight:800;
            margin-top:8px;
        ">
            Interview Portal
        </div>

        <div style="
            font-size:13px;
            color:#cbd5e1;
            margin-top:5px;
        ">
            Student Evaluation System
        </div>
    </div>
    """)

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👨‍🎓 Students",
            "📝 Evaluate Student",
            "📊 Results"
        ]
    )

    st.divider()

    show_html("""
    <div style="
        font-size:13px;
        color:#cbd5e1;
        line-height:2;
        padding:5px;
    ">
        <b>Evaluation Categories</b>

        <br><br>

        📄 CV<br>
        💪 Confidence<br>
        💬 Communication<br>
        🧠 Knowledge

        <br>

        Each category: <b>10 marks</b>
    </div>
    """)


# =========================================================
# GET STUDENT DATA
# =========================================================

students = get_students()

student_data = []

for s in students:

    total = (
        float(s["cv"]) +
        float(s["confidence"]) +
        float(s["communication"]) +
        float(s["knowledge"])
    )

    percentage = (total / 40) * 100

    student_data.append({
        "id": s["id"],
        "name": s["name"],
        "cv": float(s["cv"]),
        "confidence": float(s["confidence"]),
        "communication": float(s["communication"]),
        "knowledge": float(s["knowledge"]),
        "remark": s["remark"] or "",
        "total": total,
        "percentage": percentage
    })


df = pd.DataFrame(student_data)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    show_html("""
    <div class="hero-box">
        <div class="hero-title">
            🎓 Interview Evaluation Dashboard
        </div>

        <div class="hero-subtitle">
            Evaluate student interview performance based on
            CV, Confidence, Communication and Knowledge.
        </div>
    </div>
    """)

    total_students = len(df)

    if total_students > 0:

        evaluated_mask = (
            (df["cv"] > 0) |
            (df["confidence"] > 0) |
            (df["communication"] > 0) |
            (df["knowledge"] > 0)
        )

        evaluated_students = int(evaluated_mask.sum())

    else:

        evaluated_students = 0

    pending_students = total_students - evaluated_students

    if evaluated_students > 0:
        average_score = df.loc[
            evaluated_mask,
            "total"
        ].mean()
    else:
        average_score = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_html(f"""
        <div class="metric-box">
            <div class="metric-label">
                TOTAL STUDENTS
            </div>
            <div class="metric-number">
                {total_students}
            </div>
        </div>
        """)

    with col2:
        show_html(f"""
        <div class="metric-box">
            <div class="metric-label">
                EVALUATED
            </div>
            <div class="metric-number">
                {evaluated_students}
            </div>
        </div>
        """)

    with col3:
        show_html(f"""
        <div class="metric-box">
            <div class="metric-label">
                PENDING
            </div>
            <div class="metric-number">
                {pending_students}
            </div>
        </div>
        """)

    with col4:
        show_html(f"""
        <div class="metric-box">
            <div class="metric-label">
                AVG SCORE
            </div>
            <div class="metric-number">
                {average_score:.1f}/40
            </div>
        </div>
        """)

    show_html("""
    <div class="section-heading">
        📋 Student Overview
    </div>
    """)

    if len(df) > 0:

        overview = df[
            [
                "name",
                "cv",
                "confidence",
                "communication",
                "knowledge",
                "total",
                "percentage"
            ]
        ].copy()

        overview.columns = [
            "Student",
            "CV",
            "Confidence",
            "Communication",
            "Knowledge",
            "Total",
            "Percentage"
        ]

        overview["Percentage"] = (
            overview["Percentage"].round(1).astype(str)
            + "%"
        )

        st.dataframe(
            overview,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# STUDENTS
# =========================================================

elif page == "👨‍🎓 Students":

    show_html("""
    <div class="hero-box">
        <div class="hero-title">
            👨‍🎓 Student Management
        </div>

        <div class="hero-subtitle">
            Add, update and delete students from the system.
        </div>
    </div>
    """)

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Student",
            "✏️ Update Student",
            "🗑️ Delete Student"
        ]
    )

    # -----------------------------------------------------
    # ADD STUDENT
    # -----------------------------------------------------

    with tab1:

        st.subheader("Add New Student")

        new_name = st.text_input(
            "Student Name",
            placeholder="Enter student name",
            key="new_student"
        )

        if st.button(
            "➕ Add Student",
            use_container_width=True,
            key="add_student_button"
        ):

            if not new_name.strip():

                st.warning(
                    "Please enter a student name."
                )

            else:

                result = add_student(
                    new_name.strip()
                )

                if result:

                    st.success(
                        f"{new_name.strip()} added successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Student already exists."
                    )

    # -----------------------------------------------------
    # UPDATE STUDENT
    # -----------------------------------------------------

    with tab2:

        if len(df) > 0:

            names = df["name"].tolist()

            selected_name = st.selectbox(
                "Select Student",
                names,
                key="update_select"
            )

            selected_row = df[
                df["name"] == selected_name
            ].iloc[0]

            updated_name = st.text_input(
                "New Student Name",
                value=selected_name,
                key="updated_name"
            )

            if st.button(
                "✏️ Update Student",
                use_container_width=True,
                key="update_student_button"
            ):

                if not updated_name.strip():

                    st.warning(
                        "Student name cannot be empty."
                    )

                else:

                    result = update_student(
                        int(selected_row["id"]),
                        updated_name.strip()
                    )

                    if result:

                        st.success(
                            "Student updated successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Another student with this name already exists."
                        )

    # -----------------------------------------------------
    # DELETE STUDENT
    # -----------------------------------------------------

    with tab3:

        if len(df) > 0:

            names = df["name"].tolist()

            delete_name_selected = st.selectbox(
                "Select Student",
                names,
                key="delete_select"
            )

            delete_row = df[
                df["name"] == delete_name_selected
            ].iloc[0]

            st.warning(
                f"Deleting {delete_name_selected} will also delete "
                "their interview marks."
            )

            if st.button(
                "🗑️ Delete Student",
                use_container_width=True,
                key="delete_student_button"
            ):

                delete_student(
                    int(delete_row["id"])
                )

                st.success(
                    f"{delete_name_selected} deleted successfully!"
                )

                st.rerun()

    show_html("""
    <div class="section-heading">
        👥 All Students
    </div>
    """)

    for index, row in df.iterrows():

        show_html(f"""
        <div class="student-box">
            <div class="student-name">
                {index + 1}. {row["name"]}
            </div>
        </div>
        """)


# =========================================================
# EVALUATE STUDENT
# =========================================================

elif page == "📝 Evaluate Student":

    show_html("""
    <div class="hero-box">
        <div class="hero-title">
            📝 Interview Evaluation
        </div>

        <div class="hero-subtitle">
            Enter marks out of 10 for each category and add
            a professional remark.
        </div>
    </div>
    """)

    if len(df) == 0:

        st.info("No students available.")

    else:

        names = df["name"].tolist()

        selected_name = st.selectbox(
            "👨‍🎓 Select Student",
            names,
            key="evaluate_student"
        )

        student = df[
            df["name"] == selected_name
        ].iloc[0]

        student_id = int(student["id"])

        st.divider()

        # -------------------------------------------------
        # MARKS
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📄 CV")

            cv = st.number_input(
                "CV Marks / 10",
                min_value=0.0,
                max_value=10.0,
                value=float(student["cv"]),
                step=0.5,
                key=f"cv_{student_id}"
            )

            st.markdown("### 💬 Communication")

            communication = st.number_input(
                "Communication Marks / 10",
                min_value=0.0,
                max_value=10.0,
                value=float(student["communication"]),
                step=0.5,
                key=f"communication_{student_id}"
            )

        with col2:

            st.markdown("### 💪 Confidence")

            confidence = st.number_input(
                "Confidence Marks / 10",
                min_value=0.0,
                max_value=10.0,
                value=float(student["confidence"]),
                step=0.5,
                key=f"confidence_{student_id}"
            )

            st.markdown("### 🧠 Knowledge")

            knowledge = st.number_input(
                "Knowledge Marks / 10",
                min_value=0.0,
                max_value=10.0,
                value=float(student["knowledge"]),
                step=0.5,
                key=f"knowledge_{student_id}"
            )

        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        total = (
            cv +
            confidence +
            communication +
            knowledge
        )

        percentage = (total / 40) * 100

        if total >= 32:
            status = "Excellent"
        elif total >= 24:
            status = "Good"
        elif total >= 16:
            status = "Average"
        else:
            status = "Needs Improvement"

        st.markdown("### 📊 Current Score")

        score1, score2, score3 = st.columns(3)

        with score1:
            show_html(f"""
            <div class="score-box">
                <div class="score-title">
                    TOTAL MARKS
                </div>
                <div class="score-value">
                    {total:.1f}/40
                </div>
            </div>
            """)

        with score2:
            show_html(f"""
            <div class="score-box">
                <div class="score-title">
                    PERCENTAGE
                </div>
                <div class="score-value">
                    {percentage:.1f}%
                </div>
            </div>
            """)

        with score3:
            show_html(f"""
            <div class="score-box">
                <div class="score-title">
                    PERFORMANCE
                </div>
                <div class="score-value">
                    {status}
                </div>
            </div>
            """)

        st.markdown("### 💭 Interview Remark")

        remark = st.text_area(
            "Remark",
            value=student["remark"],
            placeholder=(
                "Example: Good communication and confidence. "
                "Technical knowledge can be improved."
            ),
            height=130,
            key=f"remark_{student_id}"
        )

        st.markdown("")

        button1, button2 = st.columns(2)

        with button1:

            if st.button(
                "💾 Save / Update Marks",
                use_container_width=True,
                key="save_marks_button"
            ):

                save_marks(
                    student_id,
                    cv,
                    confidence,
                    communication,
                    knowledge,
                    remark
                )

                st.success(
                    f"Marks saved successfully for {selected_name}!"
                )

                st.rerun()

        with button2:

            if st.button(
                "🗑️ Delete Marks",
                use_container_width=True,
                key="delete_marks_button"
            ):

                delete_marks(student_id)

                st.success(
                    f"Marks deleted for {selected_name}!"
                )

                st.rerun()


# =========================================================
# RESULTS
# =========================================================

elif page == "📊 Results":

    show_html("""
    <div class="hero-box">
        <div class="hero-title">
            📊 Interview Results
        </div>

        <div class="hero-subtitle">
            View student rankings, scores and interview remarks.
        </div>
    </div>
    """)

    if len(df) == 0:

        st.info("No students available.")

    else:

        result_df = df.sort_values(
            by="total",
            ascending=False
        ).reset_index(drop=True)

        result_df["Rank"] = range(
            1,
            len(result_df) + 1
        )

        # -------------------------------------------------
        # TOP PERFORMER
        # -------------------------------------------------

        top_student = result_df.iloc[0]

        show_html(f"""
        <div class="top-performer">

            <div class="top-title">
                🏆 TOP PERFORMER
            </div>

            <div class="top-name">
                {top_student["name"]}
            </div>

            <div class="top-score">
                {top_student["total"]:.1f} / 40
                &nbsp; • &nbsp;
                {top_student["percentage"]:.1f}%
            </div>

        </div>
        """)

        # -------------------------------------------------
        # RESULT TABLE
        # -------------------------------------------------

        result_table = result_df[
            [
                "Rank",
                "name",
                "cv",
                "confidence",
                "communication",
                "knowledge",
                "total",
                "percentage"
            ]
        ].copy()

        result_table.columns = [
            "Rank",
            "Student",
            "CV",
            "Confidence",
            "Communication",
            "Knowledge",
            "Total",
            "Percentage"
        ]

        result_table["Percentage"] = (
            result_table["Percentage"]
            .round(1)
            .astype(str)
            + "%"
        )

        st.dataframe(
            result_table,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # REMARKS
        # -------------------------------------------------

        show_html("""
        <div class="section-heading">
            💭 Student Remarks
        </div>
        """)

        for _, row in result_df.iterrows():

            remark_text = str(
                row["remark"]
            ).strip()

            if remark_text:

                show_html(f"""
                <div class="student-box">

                    <div class="student-name">
                        👨‍🎓 {row["name"]}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#475569;
                        line-height:1.6;
                    ">
                        <b>Remark:</b>
                        {remark_text}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#2563eb;
                        font-weight:700;
                        font-size:14px;
                    ">
                        Score: {row["total"]:.1f}/40
                    </div>

                </div>
                """)

            else:

                show_html(f"""
                <div class="student-box">

                    <div class="student-name">
                        👨‍🎓 {row["name"]}
                    </div>

                    <div style="
                        margin-top:8px;
                        color:#94a3b8;
                    ">
                        No remark added yet.
                    </div>

                </div>
                """)


# =========================================================
# FOOTER
# =========================================================

show_html("""
<div class="footer-box">
    Interview Evaluation System
    &nbsp;•&nbsp;
    Student Performance Management
</div>
""")