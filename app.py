import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date, datetime

from database import Base, engine, SessionLocal

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

from finance import (
    FEE_STRUCTURE,
    get_class_fee,
    get_minimum_admission_fee
)

from academics import (
    CBC_SUBJECTS,
    EXAMS,
    PROMOTION_MAP,
    calculate_grade,
    calculate_results
)

from audit import log_action


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="JAWABU LEARNING CENTRE",
    page_icon="🎓",
    layout="wide"
)


# =========================================
# BABY PINK DESIGN
# =========================================

st.markdown(
    """
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
        border: 1px solid #F3B6C8;
        border-radius: 12px;
        padding: 15px;
    }

    .stButton > button {
        background-color: #E88DAA;
        color: white;
        border-radius: 8px;
        border: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================
# CREATE DATABASE TABLES
# =========================================

Base.metadata.create_all(bind=engine)

create_default_users()


# =========================================
# SESSION STATE
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# =========================================
# REGISTRATION NUMBER
# =========================================

def generate_registration_number():

    db = SessionLocal()

    count = db.query(Student).filter(
        Student.registration_number.isnot(None)
    ).count()

    db.close()

    year = datetime.now().year

    next_number = count + 1

    return f"JLC/{year}/{next_number:04d}"


# =========================================
# LOGIN PAGE
# =========================================

def login_page():

    st.title("🎓 JAWABU LEARNING CENTRE")

    st.subheader(
        "Integrated School Management System"
    )

    st.markdown("---")

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

            st.session_state.username = user["username"]

            st.session_state.role = user["role"]

            st.success("Login successful")

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )


# =========================================
# STUDENT ADMISSION
# =========================================

def admission_page():

    st.title("📝 Student Admission")

    st.info(
        "A student must pay at least 50% of the class fee "
        "before receiving an official registration number."
    )

    with st.form("admission_form"):

        student_name = st.text_input(
            "Student Full Name"
        )

        parent_name = st.text_input(
            "Parent / Guardian Name"
        )

        parent_phone = st.text_input(
            "Parent Phone Number"
        )

        admission_date = st.date_input(
            "Admission Date",
            value=date.today()
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

        full_fee = get_class_fee(class_name)

        minimum_payment = get_minimum_admission_fee(
            class_name
        )

        st.write(
            f"### Full Fee: KES {full_fee:,.2f}"
        )

        st.write(
            f"### Minimum Admission Payment (50%): "
            f"KES {minimum_payment:,.2f}"
        )

        amount_paid = st.number_input(
            "Amount Paid",
            min_value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "PROCESS ADMISSION"
        )

    if submitted:

        if not student_name or not parent_name or not parent_phone:

            st.error(
                "Please fill in student name, parent name and phone number."
            )

            return

        db = SessionLocal()

        if amount_paid >= minimum_payment:

            registration_number = generate_registration_number()

            student = Student(

                registration_number=registration_number,

                student_name=student_name,

                parent_name=parent_name,

                parent_phone=parent_phone,

                admission_date=admission_date,

                gender=gender,

                date_of_birth=dob,

                nemis_number=nemis_number,

                class_name=class_name,

                admission_fee_paid=amount_paid,

                admission_status="ADMITTED",

                status="ACTIVE"
            )

            db.add(student)

            db.commit()

            student_id = student.id

            db.close()

            log_action(
                st.session_state.username,
                st.session_state.role,
                "CREATE",
                "STUDENTS",
                student_id,
                f"Admitted {student_name}",
                "",
                f"Registration Number: {registration_number}"
            )

            st.success(
                "Student successfully admitted."
            )

            st.success(
                f"Registration Number: {registration_number}"
            )

        else:

            student = Student(

                registration_number=None,

                student_name=student_name,

                parent_name=parent_name,

                parent_phone=parent_phone,

                admission_date=admission_date,

                gender=gender,

                date_of_birth=dob,

                nemis_number=nemis_number,

                class_name=class_name,

                admission_fee_paid=amount_paid,

                admission_status="PENDING PAYMENT",

                status="PENDING"
            )

            db.add(student)

            db.commit()

            student_id = student.id

            db.close()

            log_action(
                st.session_state.username,
                st.session_state.role,
                "CREATE",
                "PENDING ADMISSION",
                student_id,
                f"Created pending admission for {student_name}"
            )

            balance_needed = minimum_payment - amount_paid

            st.warning(
                "Student has NOT been admitted yet."
            )

            st.error(
                f"Additional KES {balance_needed:,.2f} "
                f"is required before registration number is issued."
            )


# =========================================
# PENDING ADMISSIONS
# =========================================

def pending_admissions():

    st.title("⏳ Pending Admissions")

    db = SessionLocal()

    students = db.query(Student).filter(
        Student.status == "PENDING"
    ).all()

    data = []

    for student in students:

        minimum = get_minimum_admission_fee(
            student.class_name
        )

        data.append({

            "Student Name": student.student_name,

            "Parent": student.parent_name,

            "Phone": student.parent_phone,

            "Class": student.class_name,

            "Paid": student.admission_fee_paid,

            "Minimum Required": minimum,

            "Balance Required":
                max(
                    minimum - student.admission_fee_paid,
                    0
                )
        })

    db.close()

    if data:

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True
        )

    else:

        st.success(
            "No pending admissions."
        )


# =========================================
# STUDENT SEARCH
# =========================================

def student_search():

    st.title("🔍 Student Search")

    search = st.text_input(
        "Search by Student Name, Registration Number or Parent Phone"
    )

    if search:

        db = SessionLocal()

        students = db.query(Student).filter(

            Student.student_name.ilike(
                f"%{search}%"
            )

            |

            Student.registration_number.ilike(
                f"%{search}%"
            )

            |

            Student.parent_phone.ilike(
                f"%{search}%"
            )

        ).all()

        db.close()

        if students:

            data = []

            for student in students:

                data.append({

                    "Registration Number":
                        student.registration_number,

                    "Student Name":
                        student.student_name,

                    "Parent":
                        student.parent_name,

                    "Phone":
                        student.parent_phone,

                    "Class":
                        student.class_name,

                    "Status":
                        student.status,

                    "Admission Status":
                        student.admission_status
                })

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True
            )

        else:

            st.warning(
                "No student found."
            )


# =========================================
# FINANCE - FEE STRUCTURE
# =========================================

def fee_structure_page():

    st.title("💰 School Fee Structure")

    data = []

    for class_name, fee in FEE_STRUCTURE.items():

        data.append({

            "Class": class_name,

            "Term Fee": fee,

            "50% Admission Fee": fee * 0.5
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )


# =========================================
# CREATE STUDENT BILL
# =========================================

def billing_page():

    st.title("📄 Student Fee Billing")

    db = SessionLocal()

    students = db.query(Student).filter(
        Student.status == "ACTIVE"
    ).all()

    db.close()

    if not students:

        st.warning(
            "No active students available."
        )

        return

    student_options = {

        f"{student.registration_number} - {student.student_name}":
            student

        for student in students
    }

    selected_name = st.selectbox(
        "Select Student",
        list(student_options.keys())
    )

    student = student_options[selected_name]

    term = st.selectbox(
        "Term",
        ["Term 1", "Term 2", "Term 3"]
    )

    tuition = get_class_fee(
        student.class_name
    )

    transport = st.number_input(
        "Transport Fee",
        min_value=0.0
    )

    library = st.number_input(
        "Library Fee",
        min_value=0.0
    )

    arrears = st.number_input(
        "Previous Arrears",
        min_value=0.0
    )

    total = (
        tuition +
        transport +
        library +
        arrears
    )

    st.info(
        f"Total Bill: KES {total:,.2f}"
    )

    if st.button("CREATE BILL"):

        db = SessionLocal()

        bill = Bill(

            registration_number=student.registration_number,

            class_name=student.class_name,

            term=term,

            academic_year=datetime.now().year,

            tuition_fee=tuition,

            transport_fee=transport,

            library_fee=library,

            arrears=arrears,

            total_bill=total,

            amount_paid=0,

            balance=total
        )

        db.add(bill)

        db.commit()

        bill_id = bill.id

        db.close()

        log_action(
            st.session_state.username,
            st.session_state.role,
            "CREATE",
            "BILLS",
            bill_id,
            f"Created bill for {student.student_name}",
            "",
            f"KES {total:,.2f}"
        )

        st.success(
            "Bill created successfully."
        )


# =========================================
# RECORD PAYMENT
# =========================================

def payment_page():

    st.title("💳 Fee Payments")

    db = SessionLocal()

    students = db.query(Student).filter(
        Student.status == "ACTIVE"
    ).all()

    db.close()

    if not students:

        st.warning(
            "No students available."
        )

        return

    options = {

        f"{student.registration_number} - {student.student_name}":
            student

        for student in students
    }

    selected = st.selectbox(
        "Select Student",
        list(options.keys())
    )

    student = options[selected]

    amount = st.number_input(
        "Amount Paid",
        min_value=0.0,
        step=100.0
    )

    mpesa_receipt = st.text_input(
        "M-Pesa Receipt Code"
    )

    if st.button("RECORD PAYMENT"):

        if amount <= 0:

            st.error(
                "Enter a valid payment amount."
            )

            return

        db = SessionLocal()

        payment = Payment(

            registration_number=student.registration_number,

            amount=amount,

            mpesa_receipt=mpesa_receipt if mpesa_receipt else None,

            payment_method="M-Pesa",

            status="SUCCESS",

            entered_by=st.session_state.username
        )

        db.add(payment)

        db.commit()

        payment_id = payment.id

        # Update latest outstanding bill

        bill = db.query(Bill).filter(
            Bill.registration_number ==
            student.registration_number
        ).order_by(
            Bill.id.desc()
        ).first()

        if bill:

            bill.amount_paid += amount

            bill.balance = max(
                bill.total_bill - bill.amount_paid,
                0
            )

            db.commit()

        db.close()

        log_action(
            st.session_state.username,
            st.session_state.role,
            "CREATE",
            "PAYMENTS",
            payment_id,
            f"Recorded payment for {student.student_name}",
            "",
            f"KES {amount:,.2f}"
        )

        st.success(
            "Payment recorded successfully."
        )


# =========================================
# FEE DEFAULTERS
# =========================================

def defaulters_page():

    st.title("⚠️ Fee Defaulters")

    db = SessionLocal()

    bills = db.query(Bill).filter(
        Bill.balance > 0
    ).all()

    data = []

    for bill in bills:

        student = db.query(Student).filter(
            Student.registration_number ==
            bill.registration_number
        ).first()

        if student:

            data.append({

                "Registration Number":
                    student.registration_number,

                "Student":
                    student.student_name,

                "Parent":
                    student.parent_name,

                "Phone":
                    student.parent_phone,

                "Class":
                    student.class_name,

                "Term":
                    bill.term,

                "Total Bill":
                    bill.total_bill,

                "Amount Paid":
                    bill.amount_paid,

                "Balance":
                    bill.balance
            })

    db.close()

    if data:

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True
        )

    else:

        st.success(
            "No fee defaulters."
        )


# =========================================
# EXPENSES
# =========================================

def expenses_page():

    st.title("📉 School Expenses")

    category = st.selectbox(

        "Expense Category",

        [
            "Salary",
            "Food",
            "Books",
            "Electricity",
            "WiFi",
            "Transport",
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

    if st.button("RECORD EXPENSE"):

        if amount <= 0:

            st.error(
                "Enter a valid amount."
            )

            return

        db = SessionLocal()

        expense = Expense(

            expense_date=date.today(),

            category=category,

            description=description,

            amount=amount,

            entered_by=st.session_state.username
        )

        db.add(expense)

        db.commit()

        expense_id = expense.id

        db.close()

        log_action(
            st.session_state.username,
            st.session_state.role,
            "CREATE",
            "EXPENSES",
            expense_id,
            f"Added {category} expense",
            "",
            f"KES {amount:,.2f}"
        )

        st.success(
            "Expense recorded successfully."
        )


# =========================================
# CASH FLOW GRAPH
# =========================================

def cash_flow_graph():

    st.subheader("📊 School Cash Flow")

    db = SessionLocal()

    payments = db.query(Payment).filter(
        Payment.status == "SUCCESS"
    ).all()

    expenses = db.query(Expense).all()

    db.close()

    records = []

    for payment in payments:

        records.append({

            "Date": payment.payment_date.date(),

            "Type": "Income",

            "Amount": payment.amount
        })

    for expense in expenses:

        records.append({

            "Date": expense.expense_date,

            "Type": "Expense",

            "Amount": expense.amount
        })

    if not records:

        st.info(
            "No financial transactions available."
        )

        return

    df = pd.DataFrame(records)

    grouped = df.groupby(

        ["Date", "Type"]

    )["Amount"].sum().reset_index()

    fig = px.bar(

        grouped,

        x="Date",

        y="Amount",

        color="Type",

        barmode="group",

        title="Income vs Expenses"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================
# AUDIT MONITORING
# =========================================

def audit_monitoring():

    st.title("👁️ System Activity Monitoring")

    db = SessionLocal()

    logs = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).all()

    db.close()

    data = []

    for log in logs:

        data.append({

            "Date": log.created_at,

            "User": log.username,

            "Role": log.user_role,

            "Action": log.action,

            "Module": log.table_name,

            "Description": log.description,

            "Old Value": log.old_value,

            "New Value": log.new_value
        })

    if data:

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True
        )

    else:

        st.info(
            "No activity recorded yet."
        )


# =========================================
# DIRECTOR DASHBOARD
# =========================================

def director_dashboard():

    st.title("👩‍💼 DIRECTOR CONTROL CENTRE")

    db = SessionLocal()

    total_students = db.query(Student).filter(
        Student.status == "ACTIVE"
    ).count()

    payments = db.query(Payment).filter(
        Payment.status == "SUCCESS"
    ).all()

    expenses = db.query(Expense).all()

    total_collected = sum(
        payment.amount or 0
        for payment in payments
    )

    total_expenses = sum(
        expense.amount or 0
        for expense in expenses
    )

    profit = (
        total_collected -
        total_expenses
    )

    db.close()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Active Students",
        total_students
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

    st.markdown("---")

    cash_flow_graph()


# =========================================
# TEACHER PORTAL
# =========================================

def teacher_portal():

    st.title("👩‍🏫 Teacher Academic Portal")

    db = SessionLocal()

    students = db.query(Student).filter(
        Student.status == "ACTIVE"
    ).all()

    db.close()

    if not students:

        st.warning(
            "No students available."
        )

        return

    student_options = {

        f"{student.registration_number} - {student.student_name}":
            student

        for student in students
    }

    selected = st.selectbox(
        "Select Student",
        list(student_options.keys())
    )

    student = student_options[selected]

    exam_name = st.selectbox(
        "Select Examination",
        EXAMS
    )

    term = st.selectbox(
        "Select Term",
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

    marks_data = {}

    st.subheader(
        f"Subjects for {student.class_name}"
    )

    for subject in subjects:

        marks_data[subject] = st.number_input(

            subject,

            min_value=0.0,

            max_value=100.0,

            key=f"{student.id}_{subject}_{exam_name}_{term}"
        )

    if st.button("SAVE MARKS"):

        db = SessionLocal()

        for subject, mark in marks_data.items():

            grade = calculate_grade(mark)

            record = StudentMark(

                registration_number=
                    student.registration_number,

                class_name=
                    student.class_name,

                subject=subject,

                exam_name=exam_name,

                term=term,

                academic_year=
                    datetime.now().year,

                marks=mark,

                grade=grade
            )

            db.add(record)

        db.commit()

        db.close()

        total, mean = calculate_results(
            list(marks_data.values())
        )

        log_action(
            st.session_state.username,
            st.session_state.role,
            "CREATE",
            "STUDENT MARKS",
            student.registration_number,
            f"Entered {exam_name} marks for {student.student_name}"
        )

        st.success(
            "Marks saved successfully."
        )

        st.info(
            f"Total Marks: {total} | Mean Score: {mean}"
        )


# =========================================
# PROMOTION PAGE
# =========================================

def promotion_page():

    st.title("⬆️ Student Promotion")

    current_class = st.selectbox(
        "Select Current Class",
        list(PROMOTION_MAP.keys())
    )

    next_class = PROMOTION_MAP[current_class]

    st.info(
        f"Students will be promoted from "
        f"{current_class} to {next_class}"
    )

    if st.button("PROMOTE CLASS"):

        db = SessionLocal()

        students = db.query(Student).filter(
            Student.class_name == current_class
        ).all()

        count = 0

        for student in students:

            student.class_name = next_class

            count += 1

        db.commit()

        db.close()

        log_action(
            st.session_state.username,
            st.session_state.role,
            "UPDATE",
            "STUDENT PROMOTION",
            current_class,
            f"Promoted {count} students from {current_class} to {next_class}"
        )

        st.success(
            f"{count} students promoted successfully."
        )


# =========================================
# MAIN SYSTEM
# =========================================

def main_system():

    role = st.session_state.role

    st.sidebar.title(
        "🎓 JAWABU LEARNING CENTRE"
    )

    st.sidebar.write(
        f"User: {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {role}"
    )

    st.sidebar.markdown("---")


    # =====================================
    # DIRECTOR
    # =====================================

    if role == "DIRECTOR":

        menu = st.sidebar.radio(

            "DIRECTOR MENU",

            [
                "Dashboard",
                "Student Search",
                "Cash Flow",
                "Audit Monitoring",
                "Expenses",
                "Fee Defaulters"
            ]
        )

        if menu == "Dashboard":

            director_dashboard()

        elif menu == "Student Search":

            student_search()

        elif menu == "Cash Flow":

            cash_flow_graph()

        elif menu == "Audit Monitoring":

            audit_monitoring()

        elif menu == "Expenses":

            expenses_page()

        elif menu == "Fee Defaulters":

            defaulters_page()


    # =====================================
    # ACCOUNTANT
    # =====================================

    elif role == "ACCOUNTANT":

        menu = st.sidebar.radio(

            "FINANCE MENU",

            [
                "Fee Structure",
                "Student Billing",
                "Record Payment",
                "Fee Defaulters"
            ]
        )

        if menu == "Fee Structure":

            fee_structure_page()

        elif menu == "Student Billing":

            billing_page()

        elif menu == "Record Payment":

            payment_page()

        elif menu == "Fee Defaulters":

            defaulters_page()


    # =====================================
    # RECEPTIONIST
    # =====================================

    elif role == "RECEPTIONIST":

        menu = st.sidebar.radio(

            "RECEPTION MENU",

            [
                "Student Admission",
                "Pending Admissions",
                "Student Search"
            ]
        )

        if menu == "Student Admission":

            admission_page()

        elif menu == "Pending Admissions":

            pending_admissions()

        elif menu == "Student Search":

            student_search()


    # =====================================
    # TEACHER
    # =====================================

    elif role == "TEACHER":

        menu = st.sidebar.radio(

            "ACADEMIC MENU",

            [
                "Enter Examination Marks",
                "Promote Students",
                "Student Search"
            ]
        )

        if menu == "Enter Examination Marks":

            teacher_portal()

        elif menu == "Promote Students":

            promotion_page()

        elif menu == "Student Search":

            student_search()


    # =====================================
    # LOGOUT
    # =====================================

    st.sidebar.markdown("---")

    if st.sidebar.button("LOGOUT"):

        st.session_state.clear()

        st.rerun()


# =========================================
# START APP
# =========================================

if st.session_state.logged_in:

    main_system()

else:

    login_page()
