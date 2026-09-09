import streamlit as st
import pandas as pd

from datetime import date, datetime

from database import (
    Base,
    engine,
    SessionLocal
)

from models import (
    Student,
    Bill,
    Payment,
    Expense,
    StudentMark,
    AuditLog
)

from auth import (
    create_default_users,
    login_user
)

from academics import (
    show_academics,
    CBC_SUBJECTS,
    calculate_grade,
    calculate_results,
    PROMOTION_MAP
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="JAWABU LEARNING CENTRE",

    page_icon="🎓",

    layout="wide"
)


# ==========================================
# BABY PINK DESIGN
# ==========================================

st.markdown("""

<style>

.stApp {

    background-color: #FFF5F7;

}


[data-testid="stSidebar"] {

    background-color: #F8C8DC;

}


h1, h2, h3 {

    color: #9C4F70;

}


div[data-testid="metric-container"] {

    background-color: white;

    border: 2px solid #F4B6C2;

    border-radius: 15px;

    padding: 15px;

}


.stButton > button {

    background-color: #E88DAA;

    color: white;

    border-radius: 10px;

    border: none;

}


</style>

""", unsafe_allow_html=True)


# ==========================================
# CREATE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)

create_default_users()


# ==========================================
# FEE STRUCTURE
# ==========================================

FEE_STRUCTURE = {

    "Play Group": 5000,

    "PP1": 7000,

    "PP2": 7000,

    "Grade 1": 10000,

    "Grade 2": 10000,

    "Grade 3": 10000,

    "Grade 4": 10000,

    "Grade 5": 10000,

    "Grade 6": 10000,

    "Grade 7": 12000,

    "Grade 8": 12000,

    "Grade 9": 12000
}


# ==========================================
# SCHOOL PAYMENT DETAILS
# ==========================================

SCHOOL_TILL_NUMBER = "YOUR TILL NUMBER"

SCHOOL_PAYBILL_NUMBER = "YOUR PAYBILL NUMBER"


# ==========================================
# AUTO REGISTRATION NUMBER
# ==========================================

def generate_registration_number():

    db = SessionLocal()

    count = db.query(Student).count() + 1

    year = datetime.now().year

    registration_number = (
        f"JLC/{year}/{count:04d}"
    )

    db.close()

    return registration_number


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.title("🎓 JAWABU LEARNING CENTRE")

    st.subheader(
        "School Management System"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(

        "Password",

        type="password"
    )


    if st.button("LOGIN"):

        user = login_user(

            username,

            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.username = (
                user.username
            )

            st.session_state.role = user.role

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )


# ==========================================
# ADMISSION MODULE
# ==========================================

def admission_page():

    st.title("📝 Student Admission")

    registration_number = (
        generate_registration_number()
    )

    st.info(

        f"Registration Number: "
        f"{registration_number}"
    )


    with st.form("admission_form"):

        student_name = st.text_input(
            "Student Full Name"
        )

        parent_name = st.text_input(
            "Parent/Guardian Name"
        )

        parent_phone = st.text_input(
            "Parent Phone Number"
        )

        admission_date = st.date_input(
            "Admission Date",
            date.today()
        )

        gender = st.selectbox(

            "Gender",

            ["Male", "Female"]
        )

        dob = st.date_input(
            "Date of Birth"
        )

        nemis_number = st.text_input(
            "NEMIS Number"
        )

        class_name = st.selectbox(

            "Class",

            list(FEE_STRUCTURE.keys())
        )


        submit = st.form_submit_button(
            "REGISTER STUDENT"
        )


        if submit:

            db = SessionLocal()

            student = Student(

                registration_number=
                registration_number,

                student_name=
                student_name,

                parent_name=
                parent_name,

                parent_phone=
                parent_phone,

                admission_date=
                admission_date,

                gender=
                gender,

                date_of_birth=
                dob,

                nemis_number=
                nemis_number,

                class_name=
                class_name
            )

            db.add(student)

            db.commit()

            db.close()

            st.success(
                "Student Registered Successfully!"
            )


# ==========================================
# DIRECTOR DASHBOARD
# ==========================================

def director_dashboard():

    st.title("👩‍💼 DIRECTOR DASHBOARD")

    db = SessionLocal()

    students = db.query(Student).count()

    payments = db.query(Payment).all()

    expenses = db.query(Expense).all()


    total_collected = sum(

        p.amount or 0

        for p in payments

        if p.status == "SUCCESS"
    )


    total_expenses = sum(

        e.amount or 0

        for e in expenses
    )


    profit = (
        total_collected
        - total_expenses
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(

        "Total Students",

        students
    )


    col2.metric(

        "Total Collected",

        f"KES {total_collected:,.2f}"
    )


    col3.metric(

        "Total Expenses",

        f"KES {total_expenses:,.2f}"
    )


    col4.metric(

        "Profit / Loss",

        f"KES {profit:,.2f}"
    )


    db.close()


# ==========================================
# EXPENSES
# ==========================================

def expenses_page():

    st.title("📉 Expenses")

    category = st.selectbox(

        "Expense Category",

        [

            "Salary",

            "Food",

            "Books",

            "Electricity",

            "WiFi",

            "Maintenance",

            "Other"

        ]
    )


    description = st.text_area(
        "Description"
    )


    amount = st.number_input(

        "Amount",

        min_value=0.0
    )


    if st.button(
        "RECORD EXPENSE"
    ):

        db = SessionLocal()

        expense = Expense(

            expense_date=date.today(),

            category=category,

            description=description,

            amount=amount,

            entered_by=
            st.session_state.username
        )

        db.add(expense)

        db.commit()

        db.close()

        st.success(
            "Expense Recorded Successfully"
        )


# ==========================================
# TEACHER PORTAL
# ==========================================

def teacher_portal():

    st.title("👩‍🏫 TEACHER ACADEMIC PORTAL")

    menu = st.selectbox(

        "Select Activity",

        [

            "Enter Examination Marks",

            "View Student Results",

            "Promote Students"

        ]
    )


    if menu == "Enter Examination Marks":

        db = SessionLocal()

        students = db.query(Student).all()

        db.close()


        if students:

            student_options = {

                f"{s.registration_number} - "
                f"{s.student_name}":
                s

                for s in students
            }


            selected = st.selectbox(

                "Select Student",

                list(
                    student_options.keys()
                )
            )


            student = student_options[
                selected
            ]


            exam_name = st.selectbox(

                "Examination",

                [

                    "Opening Exam",

                    "Mid Term Exam",

                    "End Term Exam"

                ]
            )


            term = st.selectbox(

                "Term",

                [

                    "Term 1",

                    "Term 2",

                    "Term 3"

                ]
            )


            subjects = CBC_SUBJECTS.get(

                student.class_name,

                []
            )


            st.subheader(
                f"Subjects - {student.class_name}"
            )


            marks_data = {}


            for subject in subjects:

                marks_data[subject] = (
                    st.number_input(

                        subject,

                        min_value=0.0,

                        max_value=100.0,

                        key=f"{student.registration_number}_{subject}_{exam_name}_{term}"
                    )
                )


            if st.button("SAVE MARKS"):

                db = SessionLocal()

                for subject, mark in marks_data.items():

                    grade = calculate_grade(
                        mark
                    )

                    record = StudentMark(

                        registration_number=
                        student.registration_number,

                        class_name=
                        student.class_name,

                        subject=
                        subject,

                        exam_name=
                        exam_name,

                        term=
                        term,

                        academic_year=
                        datetime.now().year,

                        marks=
                        mark,

                        grade=
                        grade
                    )

                    db.add(record)


                db.commit()

                db.close()

                total, mean = (
                    calculate_results(
                        list(
                            marks_data.values()
                        )
                    )
                )


                st.success(
                    "Marks Saved Successfully"
                )

                st.info(

                    f"TOTAL: {total} | "
                    f"MEAN: {mean}"
                )


    elif menu == "Promote Students":

        st.subheader(
            "Student Promotion"
        )


        selected_class = st.selectbox(

            "Select Current Class",

            list(PROMOTION_MAP.keys())
        )


        if st.button(
            "PROMOTE CLASS"
        ):

            db = SessionLocal()

            students = db.query(Student).filter(

                Student.class_name
                == selected_class

            ).all()


            next_class = PROMOTION_MAP[
                selected_class
            ]


            for student in students:

                student.class_name = (
                    next_class
                )


            db.commit()

            db.close()


            st.success(

                f"Students promoted from "
                f"{selected_class} to "
                f"{next_class}"
            )


# ==========================================
# MAIN SYSTEM
# ==========================================

def main_system():

    role = st.session_state.role


    st.sidebar.title(
        "🎓 JAWABU LEARNING CENTRE"
    )

    st.sidebar.write(

        f"Logged in as: "
        f"**{role}**"
    )


    # DIRECTOR ACCESS

    if role == "DIRECTOR":

        menu = st.sidebar.radio(

            "MENU",

            [

                "Dashboard",

                "Admission",

                "Expenses"

            ]
        )


        if menu == "Dashboard":

            director_dashboard()


        elif menu == "Admission":

            admission_page()


        elif menu == "Expenses":

            expenses_page()


    # ACCOUNTANT ACCESS

    elif role == "ACCOUNTANT":

        menu = st.sidebar.radio(

            "FINANCE MENU",

            [

                "Finance Dashboard",

                "M-Pesa",

                "Fee Billing",

                "Defaulters",

                "M-Pesa Reconciliation"

            ]
        )


        st.title(menu)

        st.info(
            "Finance modules will be integrated here."
        )


    # TEACHER ACCESS

    elif role == "TEACHER":

        teacher_portal()


    # LOGOUT

    st.sidebar.markdown("---")

    if st.sidebar.button("LOGOUT"):

        st.session_state.clear()

        st.rerun()


# ==========================================
# START APPLICATION
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if st.session_state.logged_in:

    main_system()

else:

    login_page()
